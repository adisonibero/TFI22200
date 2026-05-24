from dataclasses import dataclass, field
import math
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Station:
    """Nodo del grafo: estación o portal de TransMilenio."""

    code: str
    name: str
    station_type: str
    line: str
    x: float
    y: float


@dataclass(frozen=True)
class Edge:
    """Arista del grafo: conexión entre dos estaciones."""

    target: str
    cost: float
    rule: str
    description: str


@dataclass
class RouteStep:
    """Paso de una ruta calculada por el motor de inferencia."""

    order: int
    code: str
    name: str
    line: str
    station_type: str
    action: str
    accumulated_cost: float


@dataclass
class RouteResult:
    """Resultado final de una búsqueda desde un punto A hasta un punto B."""

    origin: str
    destination: str
    algorithm: str
    total_cost: float
    expanded_nodes: int
    steps: List[RouteStep] = field(default_factory=list)
    knowledge_rules: List[str] = field(default_factory=list)
    message: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "origin": self.origin,
            "destination": self.destination,
            "algorithm": self.algorithm,
            "total_cost": None if math.isinf(self.total_cost) else round(self.total_cost, 3),
            "expanded_nodes": self.expanded_nodes,
            "knowledge_rules": self.knowledge_rules,
            "message": self.message,
            "steps": [
                {
                    "order": step.order,
                    "code": step.code,
                    "name": step.name,
                    "line": step.line,
                    "station_type": step.station_type,
                    "action": step.action,
                    "accumulated_cost": round(step.accumulated_cost, 3),
                }
                for step in self.steps
            ],
        }
