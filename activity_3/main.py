"""CLI de la Actividad 3: aprendizaje supervisado para TransMilenio."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from activity_3.services.builder import build_dataset
from activity_3.services.model import FEATURE_COLUMNS, TransitModel

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
    """Genera el archivo CSV con datos etiquetados."""
    dataframe = build_dataset(SOURCE_JSON, DATASET_CSV)
    print_json({"mensaje": "Dataset supervisado generado", "archivo": str(DATASET_CSV), "registros": len(dataframe)})


def train_model() -> None:
    """Entrena el árbol de decisión y guarda las métricas."""
    ensure_dataset()
    model = TransitModel(DATASET_CSV)
    metrics = model.train_and_evaluate()
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "metricas.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print_json(metrics)


def predict_sample(args: argparse.Namespace) -> None:
    """Entrena el modelo y clasifica un caso ingresado por terminal."""
    ensure_dataset()
    model = TransitModel(DATASET_CSV)
    model.train_and_evaluate()
    sample = {
        "troncal": args.troncal,
        "tipo_estacion": args.tipo_estacion,
        "x_pct": args.x_pct,
        "y_pct": args.y_pct,
        "hora_pico": args.hora_pico,
        "lluvia": args.lluvia,
        "incidentes": args.incidentes,
        "demanda_estimada": args.demanda,
        "demora_historica_min": args.demora,
        "transbordos_disponibles": args.transbordos,
    }
    print_json(model.predict(sample))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Actividad 3: métodos de aprendizaje supervisado.")
    parser.add_argument("--generar-dataset", action="store_true", help="Crea el dataset supervisado en formato CSV")
    parser.add_argument("--entrenar", action="store_true", help="Entrena y evalúa el modelo supervisado")
    parser.add_argument("--predecir", action="store_true", help="Clasifica un caso operativo de ejemplo")
    parser.add_argument("--troncal", default="Suba", help="Nombre de troncal para la predicción")
    parser.add_argument("--tipo-estacion", default="portal", choices=["station", "portal"], help="Tipo de estación")
    parser.add_argument("--x-pct", type=float, default=0.20, help="Coordenada horizontal aproximada")
    parser.add_argument("--y-pct", type=float, default=0.35, help="Coordenada vertical aproximada")
    parser.add_argument("--hora-pico", type=int, default=1, choices=[0, 1], help="1 si es hora pico, 0 en otro caso")
    parser.add_argument("--lluvia", type=int, default=1, choices=[0, 1, 2], help="Nivel de lluvia: 0 bajo, 1 medio, 2 alto")
    parser.add_argument("--incidentes", type=int, default=0, help="Cantidad de incidentes reportados")
    parser.add_argument("--demanda", type=int, default=82, help="Demanda estimada entre 0 y 100")
    parser.add_argument("--demora", type=float, default=9.5, help="Demora histórica estimada en minutos")
    parser.add_argument("--transbordos", type=int, default=1, choices=[0, 1], help="1 si tiene transbordos disponibles")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.generar_dataset:
        generate_dataset()
    elif args.predecir:
        predict_sample(args)
    else:
        train_model()


if __name__ == "__main__":
    main()
