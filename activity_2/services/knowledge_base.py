import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Tuple

from models.route_models import Edge, Station
from services.text_utils import compact_name, normalize_text


@dataclass(frozen=True)
class KnowledgeRule:
    """Regla lógica de la base de conocimiento.

    Estructura conceptual usada en la actividad:
    SI se cumple una condición del sistema de transporte, ENTONCES se genera
    una acción sobre el grafo.
    """

    name: str
    condition: str
    action: str


class TransmilenioKnowledgeBase:
    """Base de conocimiento de TransMilenio representada como reglas y grafo."""

    TRANSFER_ALIASES = [
        ("Ricaurte", ["ricaurte"]),
        ("Avenida Jiménez", ["av jimenez", "avenida jimenez"]),
        ("Museo del Oro - Las Aguas - Universidades", ["museo del oro", "las aguas", "universidades"]),
        ("Centro Memoria", ["centro memoria"]),
        ("Héroes - Calle 76", ["heroes", "calle 76"]),
        ("San Victorino", ["san victorino"]),
        ("Bicentenario", ["bicentenario"]),
        ("Portal del Tunal", ["portal del tunal"]),
        ("Portal Sur", ["portal sur"]),
    ]

    def __init__(self, json_path: Path):
        self.json_path = json_path
        self.stations: Dict[str, Station] = {}
        self.graph: Dict[str, List[Edge]] = defaultdict(list)
        self.rules: List[KnowledgeRule] = [
            KnowledgeRule(
                name="R1_troncal_consecutiva",
                condition="SI dos estaciones pertenecen a la misma troncal y son consecutivas",
                action="ENTONCES se conectan en ambos sentidos con costo de desplazamiento",
            ),
            KnowledgeRule(
                name="R2_transbordo_por_nombre",
                condition="SI dos estaciones tienen nombre equivalente o pertenecen al mismo punto de intercambio",
                action="ENTONCES se agrega una conexión de transbordo con penalización baja",
            ),
            KnowledgeRule(
                name="R3_transbordo_por_cercania",
                condition="SI dos estaciones de troncales distintas están muy cerca en el mapa",
                action="ENTONCES se agrega una conexión peatonal de intercambio",
            ),
            KnowledgeRule(
                name="R4_transbordo_operativo",
                condition="SI dos estaciones conectan corredores importantes aunque el nombre sea diferente",
                action="ENTONCES se agrega una conexión manual validada como intercambio operativo",
            ),
            KnowledgeRule(
                name="R5_busqueda_optima",
                condition="SI existe un origen, un destino y un algoritmo de búsqueda",
                action="ENTONCES el motor de inferencia retorna la mejor secuencia de estaciones",
            ),
        ]
        self._load()
        self._build_graph()

    def _load(self) -> None:
        data = json.loads(self.json_path.read_text(encoding="utf-8"))
        for marker in data.get("markers", []):
            line = marker.get("line", {}) or {}
            station = Station(
                code=str(marker["code"]),
                name=str(marker["name"]),
                station_type=str(marker.get("type") or "station"),
                line=str(line.get("name") or "Sin troncal"),
                x=float(marker.get("x_pct") or 0),
                y=float(marker.get("y_pct") or 0),
            )
            self.stations[station.code] = station

    def _build_graph(self) -> None:
        self._apply_consecutive_station_rule()
        self._apply_transfer_name_rule()
        self._apply_transfer_distance_rule()
        self._apply_operational_transfer_rule()

    def _apply_consecutive_station_rule(self) -> None:
        by_line: Dict[str, List[Station]] = defaultdict(list)
        for station in self.stations.values():
            by_line[station.line].append(station)

        # El JSON viene ordenado por el recorrido de cada troncal. Por eso se conserva
        # ese orden para unir estaciones consecutivas.
        for stations in by_line.values():
            for current, next_station in zip(stations, stations[1:]):
                cost = self.distance(current.code, next_station.code) * 100 + 1
                self._connect(
                    current.code,
                    next_station.code,
                    cost,
                    "R1_troncal_consecutiva",
                    f"Avanzar por troncal {current.line}",
                )

    def _apply_transfer_name_rule(self) -> None:
        groups: Dict[str, List[Station]] = defaultdict(list)
        for station in self.stations.values():
            groups[compact_name(station.name)].append(station)

        for stations in groups.values():
            self._connect_transfer_group(stations, "R2_transbordo_por_nombre", "Transbordo por estación equivalente")

        normalized_aliases = [
            (label, [normalize_text(alias) for alias in aliases])
            for label, aliases in self.TRANSFER_ALIASES
        ]
        for label, aliases in normalized_aliases:
            stations = [
                station
                for station in self.stations.values()
                if any(alias in normalize_text(station.name) for alias in aliases)
            ]
            self._connect_transfer_group(stations, "R2_transbordo_por_nombre", f"Transbordo reconocido: {label}")

    def _apply_transfer_distance_rule(self) -> None:
        stations = list(self.stations.values())
        for i, first in enumerate(stations):
            for second in stations[i + 1 :]:
                if first.line == second.line:
                    continue
                distance = self.distance(first.code, second.code)
                if distance <= 0.040:
                    self._connect(
                        first.code,
                        second.code,
                        2.5,
                        "R3_transbordo_por_cercania",
                        "Transbordo por cercanía en mapa",
                    )


    def _apply_operational_transfer_rule(self) -> None:
        """Conexiones manuales para intersecciones principales del mapa troncal."""

        transfer_pairs = [
            ("Tercer Milenio", "Hospital"),
            ("Tygua", "Comuneros"),
            ("Banderas", "Bosa"),
            ("AV. El Dorado", "Ciudad Universitaria"),
            ("AV. Jiménez", "Museo del Oro"),
            ("San Victorino", "AV. Jiménez"),
            ("San Diego", "Museo Nacional"),
            ("Portal del Tunal", "Juan Pablo II"),
        ]

        for first_name, second_name in transfer_pairs:
            try:
                first_code = self.find_station_code(first_name)
                second_code = self.find_station_code(second_name)
            except ValueError:
                continue
            self._connect(
                first_code,
                second_code,
                3.0,
                "R4_transbordo_operativo",
                "Transbordo operativo definido en la base de conocimiento",
            )

    def _connect_transfer_group(self, stations: Iterable[Station], rule: str, description: str) -> None:
        unique = list({station.code: station for station in stations}.values())
        for i, first in enumerate(unique):
            for second in unique[i + 1 :]:
                if first.code != second.code and first.line != second.line:
                    self._connect(first.code, second.code, 2.0, rule, description)

    def _connect(self, source: str, target: str, cost: float, rule: str, description: str) -> None:
        if source == target:
            return
        self._add_edge(source, target, cost, rule, description)
        self._add_edge(target, source, cost, rule, description)

    def _add_edge(self, source: str, target: str, cost: float, rule: str, description: str) -> None:
        if any(edge.target == target and edge.rule == rule for edge in self.graph[source]):
            return
        self.graph[source].append(Edge(target=target, cost=round(cost, 4), rule=rule, description=description))

    def distance(self, source: str, target: str) -> float:
        first = self.stations[source]
        second = self.stations[target]
        return math.hypot(first.x - second.x, first.y - second.y)

    def heuristic(self, source: str, target: str) -> float:
        """Estimación para A*: distancia euclidiana sobre el mapa troncal."""

        return self.distance(source, target) * 100

    def find_station_code(self, text: str) -> str:
        """Busca una estación por código, nombre exacto o coincidencia parcial."""

        candidate = (text or "").strip()
        if not candidate:
            raise ValueError("Debe escribir una estación de origen o destino.")

        candidate_upper = candidate.upper()
        if candidate_upper in self.stations:
            return candidate_upper

        normalized = normalize_text(candidate)
        exact_matches = [
            station.code
            for station in self.stations.values()
            if normalize_text(station.name) == normalized
        ]
        if exact_matches:
            return exact_matches[0]

        partial_matches = [
            station.code
            for station in self.stations.values()
            if normalized in normalize_text(station.name)
        ]
        if len(partial_matches) == 1:
            return partial_matches[0]
        if len(partial_matches) > 1:
            names = ", ".join(self.stations[code].name for code in partial_matches[:8])
            raise ValueError(f"La búsqueda '{text}' es ambigua. Coincidencias: {names}")

        raise ValueError(f"No se encontró la estación '{text}'.")

    def list_stations(self) -> List[Dict[str, str]]:
        return [
            {
                "code": station.code,
                "name": station.name,
                "line": station.line,
                "type": station.station_type,
            }
            for station in sorted(self.stations.values(), key=lambda item: (item.line, item.name))
        ]

    def describe_rules(self) -> List[Dict[str, str]]:
        return [rule.__dict__ for rule in self.rules]

    def rule_names(self) -> List[str]:
        return [rule.name for rule in self.rules]
