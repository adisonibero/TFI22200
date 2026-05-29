<h1 align="center">🔥 Actividad 3 🧑‍💻</h1>
<h2 align="center">Métodos de aprendizaje supervisado</h2>
<h3 align="center">Clasificación del estado del servicio en TransMilenio Bogotá</h3>

## Introducción

Este proyecto implementa un modelo de aprendizaje supervisado en Python para clasificar el estado del servicio de TransMilenio. La solución usa un dataset etiquetado, creado a partir de datos de estaciones y variables operativas simuladas, para entrenar un árbol de decisión y predecir si una condición puede representar servicio normal, congestión media o congestión alta.

## Representación del problema

| Elemento | Descripción |
|---|---|
| Fuente de datos | Estaciones de TransMilenio y variables operativas simuladas. |
| Tipo de aprendizaje | Supervisado. |
| Modelo aplicado | Árbol de decisión. |
| Variable objetivo | `estado_servicio`. |
| Ejecución | Terminal. |

## Dataset

| Archivo | Descripción |
|---|---|
| `data/transmilenio.json` | Fuente base con estaciones, troncales y coordenadas. |
| `temp/dataset.csv` | Dataset generado con variables de entrada y etiqueta supervisada. |

## Modelo Implementado

| Modelo | Librería | Uso |
|---|---|---|
| `DecisionTreeClassifier` | `scikit-learn` | Clasificar el estado del servicio según las variables de entrada. |

## Requisitos

| Lenguaje de programación | Versión |
|---|---|
| Python | 3.13.x o superior |

| Librería | Uso |
|---|---|
| `pandas` | Lectura y manejo del dataset. |
| `scikit-learn` | Entrenamiento, predicción y métricas del modelo. |

## Instalación

| Sistema Operativo | Nombre del comando | Comando |
|---|---|---|
| Windows | Navegar carpeta | `cd activity_3` |
| Windows | Crear entorno virtual | `python -m venv .venv` |
| Windows | Activar entorno | `.venv\Scripts\activate` |
| Windows | Instalar dependencias | `pip install -r requirements.txt` |
| Linux o macOS | Navegar carpeta | `cd activity_3` |
| Linux o macOS | Crear entorno virtual | `python -m venv .venv` |
| Linux o macOS | Activar entorno | `source .venv/bin/activate` |
| Linux o macOS | Instalar dependencias | `pip install -r requirements.txt` |

## Ejecución Terminal

| Acción | Comando |
|---|---|
| Generar dataset | `python main.py --generar-dataset` |
| Entrenar y evaluar | `python main.py --entrenar` |
| Ejecutar predicción | `python main.py --predecir --troncal "Suba" --tipo-estacion portal --hora-pico 1 --lluvia 2 --incidentes 1 --demanda 92 --demora 15 --transbordos 1` |

# Datos Detallados

| Campo | Tipo | Descripción |
|---|---|---|
| `codigo_estacion` | Texto | Código interno de la estación. |
| `nombre_estacion` | Texto | Nombre de la estación o portal. |
| `troncal` | Texto | Línea o troncal a la que pertenece la estación. |
| `tipo_estacion` | Texto | Indica si el punto es estación o portal. |
| `x_pct` | Numérico | Coordenada horizontal aproximada en el mapa. |
| `y_pct` | Numérico | Coordenada vertical aproximada en el mapa. |
| `hora_pico` | Numérico | Valor 1 para hora pico y 0 para horario normal. |
| `lluvia` | Numérico | Nivel de lluvia entre 0 y 2. |
| `incidentes` | Numérico | Cantidad estimada de incidentes operativos. |
| `demanda_estimada` | Numérico | Estimación de demanda entre 0 y 100. |
| `demora_historica_min` | Numérico | Demora histórica aproximada en minutos. |
| `transbordos_disponibles` | Numérico | Valor 1 cuando hay opción de cambio o conexión. |
| `estado_servicio` | Texto | Etiqueta supervisada: servicio normal, congestión media o congestión alta. |

## Estructura Organizada

```txt
activity_3/
├── data/
│   ├── transmilenio.json
├── outputs/
│   └── metricas.json
│   └── transmilenio.csv
├── services/
│   ├── __init__.py
│   ├── builder.py
│   └── model.py
├── main.py
├── README.md
└── requirements.txt
```

## Procedimiento del sistema

1. Se carga la información base de TransMilenio.
2. Se construye un dataset etiquetado con variables operativas.
3. Se separan datos de entrenamiento y prueba.
4. Se entrena un árbol de decisión.
5. Se calculan métricas de evaluación.
6. Se permite clasificar nuevos casos desde la terminal.

## Pruebas Ejecutadas

| Prueba | Comando | Resultado esperado |
|---|---|---|
| 1 | `python main.py --generar-dataset` | Genera el archivo CSV supervisado. |
| 2 | `python main.py --entrenar` | Entrena el árbol de decisión y muestra exactitud, matriz de confusión y reporte de clasificación. |
| 3 | `python main.py --predecir --troncal "Suba" --tipo-estacion portal --hora-pico 1 --lluvia 2 --incidentes 1 --demanda 92 --demora 15 --transbordos 1` | Predice el estado del servicio para un caso de alta demanda. |
| 4 | `python main.py --predecir --troncal "Calle 80" --tipo-estacion station --hora-pico 0 --lluvia 0 --incidentes 0 --demanda 45 --demora 3 --transbordos 0` | Predice el estado del servicio para un caso estable. |
| 5 | `python main.py --predecir --troncal "Caracas" --tipo-estacion station --hora-pico 1 --lluvia 1 --incidentes 0 --demanda 70 --demora 8 --transbordos 1` | Predice el estado del servicio para un caso de congestión media. |
| 6 | `python main.py --predecir --troncal "Américas" --tipo-estacion portal --hora-pico 1 --lluvia 2 --incidentes 2 --demanda 96 --demora 20 --transbordos 1` | Predice el estado del servicio para un caso crítico de alta congestión. |
