"""CLI de la Actividad 4: aprendizaje no supervisado para TransMilenio."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from activity_4.services.builder import build_dataset
from activity_4.services.model import TransitModel

BASE_DIR = Path(__file__).resolve().parent
SOURCE_JSON = BASE_DIR / "data" / "transmilenio.json"
DATASET_CSV = BASE_DIR / "temp" / "dataset.csv"
OUTPUT_DIR = BASE_DIR / "temp"


def print_json(data: dict) -> None:
    """Imprime datos en formato JSON legible."""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def ensure_dataset() -> None:
    """Crea el dataset cuando todavía no existe."""
    if not DATASET_CSV.exists():
        build_dataset(SOURCE_JSON, DATASET_CSV)


def generate_dataset() -> None:
    """Genera el archivo CSV sin etiquetas."""
    dataframe = build_dataset(SOURCE_JSON, DATASET_CSV)
    print_json({"mensaje": "Dataset no supervisado generado", "archivo": str(DATASET_CSV), "registros": len(dataframe)})


def cluster_stations(clusters: int) -> None:
    """Agrupa estaciones y guarda los resultados."""
    ensure_dataset()
    model = TransitModel(DATASET_CSV, clusters=clusters)
    metrics, grouped = model.cluster()
    OUTPUT_DIR.mkdir(exist_ok=True)
    grouped.to_csv(OUTPUT_DIR / "agrupados.csv", index=False, encoding="utf-8")
    (OUTPUT_DIR / "metricas.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print_json(metrics)


def predict_group(args: argparse.Namespace) -> None:
    """Asigna un nuevo caso operativo a un grupo."""
    ensure_dataset()
    model = TransitModel(DATASET_CSV, clusters=args.clusters)
    sample = {
        "troncal": args.troncal,
        "tipo_estacion": args.tipo_estacion,
        "x_pct": args.x_pct,
        "y_pct": args.y_pct,
        "es_portal": args.es_portal,
        "posible_transbordo": args.posible_transbordo,
        "demanda_estimada": args.demanda,
        "demora_promedio_min": args.demora,
        "frecuencia_buses_min": args.frecuencia,
    }
    print_json(model.predict_group(sample))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Actividad 4: métodos de aprendizaje no supervisado.")
    parser.add_argument("--generar-dataset", action="store_true", help="Crea el dataset no supervisado en formato CSV")
    parser.add_argument("--agrupar", action="store_true", help="Ejecuta K-Means sobre las estaciones")
    parser.add_argument("--predecir-grupo", action="store_true", help="Asigna un caso operativo a un grupo")
    parser.add_argument("--clusters", type=int, default=3, help="Cantidad de grupos para K-Means")
    parser.add_argument("--troncal", default="Suba", help="Nombre de troncal")
    parser.add_argument("--tipo-estacion", default="portal", choices=["station", "portal"], help="Tipo de estación")
    parser.add_argument("--x-pct", type=float, default=0.20, help="Coordenada horizontal aproximada")
    parser.add_argument("--y-pct", type=float, default=0.35, help="Coordenada vertical aproximada")
    parser.add_argument("--es-portal", type=int, default=1, choices=[0, 1], help="1 si el punto es portal")
    parser.add_argument("--posible-transbordo", type=int, default=1, choices=[0, 1], help="1 si tiene conexión o cambio")
    parser.add_argument("--demanda", type=int, default=88, help="Demanda estimada entre 0 y 100")
    parser.add_argument("--demora", type=float, default=13.0, help="Demora promedio estimada")
    parser.add_argument("--frecuencia", type=float, default=4.0, help="Frecuencia promedio de buses")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.generar_dataset:
        generate_dataset()
    elif args.predecir_grupo:
        predict_group(args)
    else:
        cluster_stations(args.clusters)


if __name__ == "__main__":
    main()
