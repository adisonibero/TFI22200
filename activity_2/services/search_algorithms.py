"""Implementacion de BFS, DFS, Dijkstra y A* para el grafo de estaciones."""

import heapq
from collections import deque
from math import inf
from typing import Callable, Dict, List, Optional, Set, Tuple

from models.route_models import Edge


class SearchAlgorithms:
    """Algoritmos de búsqueda usados por el sistema inteligente."""

    @staticmethod
    def bfs(graph: Dict[str, List[Edge]], start: str, goal: str) -> Tuple[List[str], float, int]:
        """Busqueda en anchura priorizando la menor cantidad de pasos."""
        queue = deque([(start, [start], 0.0)])
        visited: Set[str] = {start}
        expanded = 0

        while queue:
            current, path, cost = queue.popleft()
            expanded += 1
            if current == goal:
                return path, cost, expanded
            for edge in graph.get(current, []):
                if edge.target not in visited:
                    visited.add(edge.target)
                    queue.append((edge.target, path + [edge.target], cost + edge.cost))
        return [], inf, expanded

    @staticmethod
    def dfs(graph: Dict[str, List[Edge]], start: str, goal: str) -> Tuple[List[str], float, int]:
        """Busqueda en profundidad sobre el grafo."""
        stack = [(start, [start], 0.0)]
        visited: Set[str] = set()
        expanded = 0

        while stack:
            current, path, cost = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            expanded += 1
            if current == goal:
                return path, cost, expanded
            for edge in reversed(graph.get(current, [])):
                if edge.target not in visited:
                    stack.append((edge.target, path + [edge.target], cost + edge.cost))
        return [], inf, expanded

    @staticmethod
    def dijkstra(graph: Dict[str, List[Edge]], start: str, goal: str) -> Tuple[List[str], float, int]:
        """Busqueda de costo minimo sin heuristica."""
        return SearchAlgorithms._weighted_search(graph, start, goal, lambda _node: 0.0)

    @staticmethod
    def astar(
        graph: Dict[str, List[Edge]],
        start: str,
        goal: str,
        heuristic: Callable[[str], float],
    ) -> Tuple[List[str], float, int]:
        """Busqueda A* combinando costo acumulado y heuristica."""
        return SearchAlgorithms._weighted_search(graph, start, goal, heuristic)

    @staticmethod
    def _weighted_search(
        graph: Dict[str, List[Edge]],
        start: str,
        goal: str,
        heuristic: Callable[[str], float],
    ) -> Tuple[List[str], float, int]:
        """Nucleo compartido para Dijkstra y A* usando cola de prioridad."""
        open_heap: List[Tuple[float, float, str]] = [(heuristic(start), 0.0, start)]
        came_from: Dict[str, Optional[str]] = {start: None}
        cost_so_far: Dict[str, float] = {start: 0.0}
        expanded = 0

        while open_heap:
            _priority, current_cost, current = heapq.heappop(open_heap)
            if current_cost > cost_so_far.get(current, inf):
                continue
            expanded += 1
            if current == goal:
                return SearchAlgorithms._reconstruct_path(came_from, goal), cost_so_far[goal], expanded

            for edge in graph.get(current, []):
                new_cost = cost_so_far[current] + edge.cost
                if new_cost < cost_so_far.get(edge.target, inf):
                    cost_so_far[edge.target] = new_cost
                    priority = new_cost + heuristic(edge.target)
                    heapq.heappush(open_heap, (priority, new_cost, edge.target))
                    came_from[edge.target] = current

        return [], inf, expanded

    @staticmethod
    def _reconstruct_path(came_from: Dict[str, Optional[str]], goal: str) -> List[str]:
        """Reconstruye la ruta final desde el objetivo hasta el origen."""
        path = [goal]
        current = goal
        while came_from[current] is not None:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
