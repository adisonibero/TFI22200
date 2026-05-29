"""Modelo supervisado para clasificar el estado del servicio."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier, export_text

FEATURE_COLUMNS = [
    "troncal",
    "tipo_estacion",
    "x_pct",
    "y_pct",
    "hora_pico",
    "lluvia",
    "incidentes",
    "demanda_estimada",
    "demora_historica_min",
    "transbordos_disponibles",
]
TARGET_COLUMN = "estado_servicio"
CATEGORICAL_COLUMNS = ["troncal", "tipo_estacion"]
NUMERIC_COLUMNS = [column for column in FEATURE_COLUMNS if column not in CATEGORICAL_COLUMNS]


class TransitModel:
    """Entrena y evalúa un árbol de decisión sobre datos etiquetados."""

    def __init__(self, csv_path: Path) -> None:
        self.csv_path = csv_path
        self.dataframe = pd.read_csv(csv_path)
        self.pipeline = self._build_pipeline()

    def _build_pipeline(self) -> Pipeline:
        preprocessor = ColumnTransformer(
            transformers=[
                ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLUMNS),
                ("numeric", "passthrough", NUMERIC_COLUMNS),
            ]
        )
        classifier = DecisionTreeClassifier(max_depth=5, random_state=42)
        return Pipeline(steps=[("preprocessor", preprocessor), ("classifier", classifier)])

    def train_and_evaluate(self) -> dict:
        """Entrena el modelo y retorna métricas de evaluación."""
        x = self.dataframe[FEATURE_COLUMNS]
        y = self.dataframe[TARGET_COLUMN]
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.25, random_state=42, stratify=y
        )

        self.pipeline.fit(x_train, y_train)
        predictions = self.pipeline.predict(x_test)

        tree_rules = export_text(
            self.pipeline.named_steps["classifier"],
            feature_names=self.pipeline.named_steps["preprocessor"].get_feature_names_out().tolist(),
        )

        return {
            "modelo": "DecisionTreeClassifier",
            "tipo_aprendizaje": "supervisado",
            "total_registros": int(len(self.dataframe)),
            "registros_entrenamiento": int(len(x_train)),
            "registros_prueba": int(len(x_test)),
            "exactitud": round(float(accuracy_score(y_test, predictions)), 4),
            "matriz_confusion": confusion_matrix(y_test, predictions).tolist(),
            "reporte_clasificacion": classification_report(y_test, predictions, output_dict=True, zero_division=0),
            "reglas_arbol_decision": tree_rules,
        }

    def predict(self, sample: dict) -> dict:
        """Clasifica un nuevo caso operativo ingresado por terminal."""
        sample_frame = pd.DataFrame([sample], columns=FEATURE_COLUMNS)
        prediction = self.pipeline.predict(sample_frame)[0]
        probabilities = self.pipeline.predict_proba(sample_frame)[0]
        classes = self.pipeline.named_steps["classifier"].classes_
        return {
            "entrada": sample,
            "prediccion": prediction,
            "probabilidades": {str(label): round(float(value), 4) for label, value in zip(classes, probabilities)},
        }
