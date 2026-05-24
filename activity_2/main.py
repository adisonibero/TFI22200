"""CLI para consultar rutas de TransMilenio con varios algoritmos de busqueda."""

import argparse
import json
from typing import List

from services.inference_engine import RouteInferenceEngine


ALGORITHMS = ["astar", "dijkstra", "bfs", "dfs"]


def print_json(data: dict) -> None:
    """Imprime diccionarios en formato JSON legible para la terminal."""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def run_cli(origin: str, destination: str, algorithm: str) -> None:
    """
    Ejecuta el sistema inteligente desde terminal.

    Procedimiento:
    1. Carga la base de conocimiento de TransMilenio desde data/transmilenio.json.
    2. Construye el grafo de estaciones y conexiones mediante reglas lógicas.
    3. Ejecuta el motor de inferencia con el algoritmo seleccionado.
    4. Muestra la mejor ruta encontrada desde el origen hasta el destino.
    """

    engine = RouteInferenceEngine.from_default_data()
    result = engine.find_route(origin, destination, algorithm)
    print_json(result.to_dict())


def list_stations() -> None:
    """Lista las estaciones disponibles en la base de conocimiento."""
    engine = RouteInferenceEngine.from_default_data()
    stations: List[dict] = [
        {
            "code": station.code,
            "name": station.name,
            "line": station.line,
            "type": station.station_type,
        }
        for station in sorted(engine.knowledge_base.stations.values(), key=lambda item: item.name)
    ]
    print_json({"total": len(stations), "stations": stations})


def show_rules() -> None:
    """Muestra las reglas lógicas usadas por la base de conocimiento."""
    engine = RouteInferenceEngine.from_default_data()
    print_json({"knowledge_rules": engine.knowledge_base.rule_names()})


def parse_args() -> argparse.Namespace:
    """Construye y parsea los argumentos de linea de comandos."""
    parser = argparse.ArgumentParser(
        description="Actividad 2: búsqueda y sistema basado en reglas para rutas de TransMilenio."
    )
    parser.add_argument("--origen", "--origin", dest="origin", help="Nombre de la estación origen")
    parser.add_argument("--destino", "--destination", dest="destination", help="Nombre de la estación destino")
    parser.add_argument(
        "--algoritmo",
        "--algorithm",
        dest="algorithm",
        default="astar",
        choices=ALGORITHMS,
        help="Algoritmo de búsqueda a ejecutar: astar, dijkstra, bfs o dfs",
    )
    parser.add_argument(
        "--listar-estaciones",
        action="store_true",
        help="Muestra las estaciones disponibles en la base de conocimiento",
    )
    parser.add_argument(
        "--ver-reglas",
        action="store_true",
        help="Muestra las reglas lógicas del sistema basado en conocimiento",
    )
    return parser.parse_args()


def main() -> None:
    """Punto de entrada principal del programa en modo terminal."""
    args = parse_args()

    try:
        if args.listar_estaciones:
            list_stations()
            return

        if args.ver_reglas:
            show_rules()
            return

        if not args.origin or not args.destination:
            print("Debe indicar origen y destino para calcular una ruta.\n")
            print("Ejemplo:")
            print('python main.py --origen "Portal del Norte" --destino "Universidades" --algoritmo astar')
            print("\nComandos de apoyo:")
            print("python main.py --listar-estaciones")
            print("python main.py --ver-reglas")
            return

        run_cli(args.origin, args.destination, args.algorithm)
    except ValueError as error:
        print_json({"error": str(error)})


if __name__ == "__main__":
    main()
