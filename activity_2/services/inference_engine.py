"""Motor de inferencia para resolver rutas sobre la base de conocimiento."""

from math import inf
from pathlib import Path
from typing import List, Optional

from models.route_models import RouteResult, RouteStep
from services.knowledge_base import TransmilenioKnowledgeBase
from services.search_algorithms import SearchAlgorithms


class RouteInferenceEngine:
    """Motor de inferencia para consultar la base de conocimiento y calcular rutas."""

    def __init__(self, knowledge_base: TransmilenioKnowledgeBase):
        self.knowledge_base = knowledge_base

    @classmethod
    def from_default_data(cls) -> "RouteInferenceEngine":
        """Crea una instancia usando el archivo JSON por defecto del proyecto."""
        json_path = Path(__file__).resolve().parents[1] / "data" / "transmilenio.json"
        return cls(TransmilenioKnowledgeBase(json_path))

    def find_route(self, origin: str, destination: str, algorithm: str = "astar") -> RouteResult:
        """Calcula una ruta entre dos estaciones con el algoritmo seleccionado."""
        start_code = self.knowledge_base.find_station_code(origin)
        goal_code = self.knowledge_base.find_station_code(destination)
        selected_algorithm = (algorithm or "astar").strip().lower()

        if selected_algorithm == "bfs":
            path, total_cost, expanded = SearchAlgorithms.bfs(self.knowledge_base.graph, start_code, goal_code)
        elif selected_algorithm == "dfs":
            path, total_cost, expanded = SearchAlgorithms.dfs(self.knowledge_base.graph, start_code, goal_code)
        elif selected_algorithm == "dijkstra":
            path, total_cost, expanded = SearchAlgorithms.dijkstra(self.knowledge_base.graph, start_code, goal_code)
        elif selected_algorithm in {"astar", "a_star", "a*"}:
            path, total_cost, expanded = SearchAlgorithms.astar(
                self.knowledge_base.graph,
                start_code,
                goal_code,
                lambda node: self.knowledge_base.heuristic(node, goal_code),
            )
            selected_algorithm = "astar"
        else:
            raise ValueError("Algoritmo no soportado. Use: astar, dijkstra, bfs o dfs.")

        if not path or total_cost == inf:
            return RouteResult(
                origin=self.knowledge_base.stations[start_code].name,
                destination=self.knowledge_base.stations[goal_code].name,
                algorithm=selected_algorithm,
                total_cost=inf,
                expanded_nodes=expanded,
                knowledge_rules=self.knowledge_base.rule_names(),
                message="No se encontró una ruta con la base de conocimiento actual.",
            )

        return RouteResult(
            origin=self.knowledge_base.stations[start_code].name,
            destination=self.knowledge_base.stations[goal_code].name,
            algorithm=selected_algorithm,
            total_cost=total_cost,
            expanded_nodes=expanded,
            steps=self._build_steps(path),
            knowledge_rules=self.knowledge_base.rule_names(),
            message="Ruta encontrada correctamente.",
        )

    def _build_steps(self, path: List[str]) -> List[RouteStep]:
        """Convierte una secuencia de codigos en pasos detallados de ruta."""
        steps: List[RouteStep] = []
        accumulated = 0.0

        for index, code in enumerate(path):
            station = self.knowledge_base.stations[code]
            action = "Inicio" if index == 0 else self._edge_description(path[index - 1], code)
            if index > 0:
                accumulated += self._edge_cost(path[index - 1], code)
            steps.append(
                RouteStep(
                    order=index + 1,
                    code=station.code,
                    name=station.name,
                    line=station.line,
                    station_type=station.station_type,
                    action=action,
                    accumulated_cost=accumulated,
                )
            )
        return steps

    def _edge_description(self, source: str, target: str) -> str:
        """Obtiene la descripcion de la transicion entre dos estaciones."""
        edge = self._find_edge(source, target)
        return f"{edge.description} ({edge.rule})" if edge else "Avanzar"

    def _edge_cost(self, source: str, target: str) -> float:
        """Retorna el costo de moverse desde source hasta target."""
        edge = self._find_edge(source, target)
        return edge.cost if edge else 0.0

    def _find_edge(self, source: str, target: str):
        """Busca la arista directa entre una estacion origen y una destino."""
        for edge in self.knowledge_base.graph.get(source, []):
            if edge.target == target:
                return edge
        return None
