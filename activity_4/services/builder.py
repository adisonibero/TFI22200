"""Construcción del dataset no supervisado para TransMilenio."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def _line_name(marker: dict) -> str:
    line = marker.get("line") or {}
    return line.get("name") or "Sin troncal"


def build_dataset(source_json: Path, output_csv: Path) -> pd.DataFrame:
    """Crea un dataset sin etiquetas para aplicar agrupamiento."""
    with source_json.open("r", encoding="utf-8") as file:
        data = json.load(file)

    rows: list[dict] = []
    for index, marker in enumerate(data.get("markers", [])):
        station_type = marker.get("type") or "station"
        line = _line_name(marker)
        x_pct = float(marker.get("x_pct", 0))
        y_pct = float(marker.get("y_pct", 0))
        portal_factor = 1 if station_type == "portal" else 0
        transfer_factor = 1 if any(token in marker.get("name", "").lower() for token in ["portal", "calle", "avenida", "carrera"]) else 0

        rows.append(
            {
                "codigo_estacion": marker.get("code"),
                "nombre_estacion": marker.get("name"),
                "troncal": line,
                "tipo_estacion": station_type,
                "x_pct": round(x_pct, 5),
                "y_pct": round(y_pct, 5),
                "es_portal": portal_factor,
                "posible_transbordo": transfer_factor,
                "demanda_estimada": min(100, 38 + portal_factor * 24 + transfer_factor * 12 + (index % 9) * 4),
                "demora_promedio_min": round(3.0 + portal_factor * 4.5 + transfer_factor * 2.5 + (index % 7) * 0.9, 2),
                "frecuencia_buses_min": round(2.5 + (index % 6) * 0.8 + portal_factor * 0.5, 2),
            }
        )

    dataframe = pd.DataFrame(rows)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_csv, index=False, encoding="utf-8")
    return dataframe
