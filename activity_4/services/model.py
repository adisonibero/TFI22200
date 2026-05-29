"""Modelo no supervisado para agrupar estaciones de TransMilenio."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

FEATURE_COLUMNS = [
    "troncal",
    "tipo_estacion",
    "x_pct",
    "y_pct",
    "es_portal",
    "posible_transbordo",
    "demanda_estimada",
    "demora_promedio_min",
    "frecuencia_buses_min",
]
CATEGORICAL_COLUMNS = ["troncal", "tipo_estacion"]
NUMERIC_COLUMNS = [column for column in FEATURE_COLUMNS if column not in CATEGORICAL_COLUMNS]


class TransitModel:
    """Aplica agrupamiento K-Means sobre estaciones sin etiqueta previa."""

    def __init__(self, csv_path: Path, clusters: int = 3) -> None:
        self.csv_path = csv_path
        self.clusters = clusters
        self.dataframe = pd.read_csv(csv_path)
        self.pipeline = self._build_pipeline()

    def _build_pipeline(self) -> Pipeline:
        preprocessor = ColumnTransformer(
            transformers=[
                ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLUMNS),
                ("numeric", StandardScaler(), NUMERIC_COLUMNS),
            ]
        )
        model = KMeans(n_clusters=self.clusters, random_state=42, n_init=10)
        return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])

    def cluster(self) -> tuple[dict, pd.DataFrame]:
        """Agrupa estaciones y retorna resumen junto con el dataset etiquetado por grupo."""
        x = self.dataframe[FEATURE_COLUMNS]
        labels = self.pipeline.fit_predict(x)
        result = self.dataframe.copy()
        result["grupo"] = labels

        transformed = self.pipeline.named_steps["preprocessor"].transform(x)
        silhouette = silhouette_score(transformed, labels) if self.clusters > 1 else 0

        summaries = []
        for group_id, group in result.groupby("grupo"):
            summaries.append(
                {
                    "grupo": int(group_id),
                    "cantidad_estaciones": int(len(group)),
                    "demanda_promedio": round(float(group["demanda_estimada"].mean()), 2),
                    "demora_promedio_min": round(float(group["demora_promedio_min"].mean()), 2),
                    "frecuencia_promedio_min": round(float(group["frecuencia_buses_min"].mean()), 2),
                    "ejemplos_estaciones": group["nombre_estacion"].head(5).tolist(),
                }
            )

        metrics = {
            "modelo": "KMeans",
            "tipo_aprendizaje": "no supervisado",
            "clusters": self.clusters,
            "total_estaciones": int(len(result)),
            "silhouette_score": round(float(silhouette), 4),
            "resumen_grupos": summaries,
        }
        return metrics, result

    def predict_group(self, sample: dict) -> dict:
        """Asigna un nuevo caso al grupo más cercano."""
        self.cluster()
        sample_frame = pd.DataFrame([sample], columns=FEATURE_COLUMNS)
        group = int(self.pipeline.predict(sample_frame)[0])
        return {"entrada": sample, "grupo_asignado": group}
