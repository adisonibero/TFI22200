"""Construcción del dataset supervisado para TransMilenio."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def _line_name(marker: dict) -> str:
    line = marker.get("line") or {}
    return line.get("name") or "Sin troncal"


def _station_type(marker: dict) -> str:
    return marker.get("type") or "station"


def _base_demand(marker: dict) -> int:
    """Estima demanda base con datos disponibles del punto de parada."""
    station_type = _station_type(marker)
    line = _line_name(marker).lower()
    demand = 45

    if station_type == "portal":
        demand += 25
    if any(word in line for word in ["caracas", "nqs", "autonorte", "américas", "suba"]):
        demand += 12
    if marker.get("x_pct", 0) > 0.45:
        demand += 5
    if marker.get("y_pct", 0) > 0.60:
        demand += 4

    return min(demand, 95)


def _label_service(row: dict) -> str:
    """Etiqueta supervisada calculada para simular el estado esperado del servicio."""
    score = 0
    score += row["demanda_estimada"] * 0.45
    score += row["demora_historica_min"] * 2.0
    score += row["incidentes"] * 9
    score += row["lluvia"] * 6
    score += row["hora_pico"] * 12
    score += row["transbordos_disponibles"] * 3

    if score >= 85:
        return "congestion_alta"
    if score >= 62:
        return "congestion_media"
    return "servicio_normal"


def build_dataset(source_json: Path, output_csv: Path) -> pd.DataFrame:
    """Crea un dataset etiquetado a partir de las estaciones de TransMilenio."""
    with source_json.open("r", encoding="utf-8") as file:
        data = json.load(file)

    rows: list[dict] = []
    markers = data.get("markers", [])
    for index, marker in enumerate(markers):
        name = marker.get("name", "Sin nombre")
        line = _line_name(marker)
        station_type = _station_type(marker)
        base_demand = _base_demand(marker)
        transfer_hint = 1 if any(token in name.lower() for token in ["portal", "avenida", "calle", "carrera"]) else 0

        for peak_hour in [0, 1]:
            for rain_level in [0, 1, 2]:
                incident_count = 1 if (index + peak_hour + rain_level) % 11 == 0 else 0
                historical_delay = round(2 + rain_level * 2.4 + peak_hour * 4.2 + incident_count * 7.0 + (index % 5) * 0.8, 2)
                demand = min(100, base_demand + peak_hour * 13 + rain_level * 3 + incident_count * 5)
                row = {
                    "codigo_estacion": marker.get("code"),
                    "nombre_estacion": name,
                    "troncal": line,
                    "tipo_estacion": station_type,
                    "x_pct": round(float(marker.get("x_pct", 0)), 5),
                    "y_pct": round(float(marker.get("y_pct", 0)), 5),
                    "hora_pico": peak_hour,
                    "lluvia": rain_level,
                    "incidentes": incident_count,
                    "demanda_estimada": demand,
                    "demora_historica_min": historical_delay,
                    "transbordos_disponibles": transfer_hint,
                }
                row["estado_servicio"] = _label_service(row)
                rows.append(row)

    dataframe = pd.DataFrame(rows)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_csv, index=False, encoding="utf-8")
    return dataframe
