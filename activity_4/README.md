<h1 align="center">🔥 Actividad 4 🧑‍💻</h1>
<h2 align="center">Métodos de aprendizaje no supervisado</h2>
<h3 align="center">Agrupamiento de estaciones de TransMilenio Bogotá</h3>

## Introducción

Este proyecto implementa un modelo de aprendizaje no supervisado en Python para agrupar estaciones de TransMilenio según características operativas. La solución usa un dataset sin etiqueta objetivo y aplica K-Means para identificar grupos de estaciones con comportamientos similares.

## Representación del problema

| Elemento | Descripción |
|---|---|
| Fuente de datos | Estaciones de TransMilenio y variables operativas simuladas. |
| Tipo de aprendizaje | No supervisado. |
| Modelo aplicado | K-Means. |
| Salida | Grupo asignado a cada estación. |
| Ejecución | Terminal. |

## Dataset

| Archivo | Descripción |
|---|---|
| `data/transmilenio.json` | Fuente base con estaciones, troncales y coordenadas. |
| `temp/dataset.csv` | Dataset generado sin etiqueta objetivo. |

## Modelo Implementado

| Modelo | Librería | Uso |
|---|---|---|
| `KMeans` | `scikit-learn` | Agrupar estaciones con características similares. |

## Requisitos

| Lenguaje de programación | Versión |
|---|---|
| Python | 3.13.x o superior |

| Librería | Uso |
|---|---|
| `pandas` | Lectura y manejo del dataset. |
| `scikit-learn` | Agrupamiento y métrica de evaluación. |

## Instalación

| Sistema Operativo | Nombre del comando | Comando |
|---|---|---|
| Windows | Navegar carpeta | `cd activity_4` |
| Windows | Crear entorno virtual | `python -m venv .venv` |
| Windows | Activar entorno | `.venv\Scripts\activate` |
| Windows | Instalar dependencias | `pip install -r requirements.txt` |
| Linux o macOS | Navegar carpeta | `cd activity_4` |
| Linux o macOS | Crear entorno virtual | `python -m venv .venv` |
| Linux o macOS | Activar entorno | `source .venv/bin/activate` |
| Linux o macOS | Instalar dependencias | `pip install -r requirements.txt` |

## Ejecución Terminal

| Acción | Comando |
|---|---|
| Generar dataset | `python main.py --generar-dataset` |
| Agrupar estaciones | `python main.py --agrupar --clusters 3` |
| Agrupar con otra cantidad | `python main.py --agrupar --clusters 4` |
| Asignar grupo a un caso | `python main.py --predecir-grupo --clusters 3 --troncal "Suba" --tipo-estacion portal --es-portal 1 --posible-transbordo 1 --demanda 88 --demora 13 --frecuencia 4` |

## Estructura Organizada

```txt
activity_4/
├── data/
│   ├── transmilenio.json
├── temp/
│   └── dataset.csv
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
2. Se construye un dataset sin etiqueta objetivo.
3. Se seleccionan variables numéricas y categóricas.
4. Se normalizan los datos.
5. Se aplica K-Means para crear grupos.
6. Se muestran métricas y ejemplos de estaciones por grupo.

# Datos Detallados

| Campo | Tipo | Descripción |
|---|---|---|
| `codigo_estacion` | Texto | Código interno de la estación. |
| `nombre_estacion` | Texto | Nombre de la estación o portal. |
| `troncal` | Texto | Línea o troncal de la estación. |
| `tipo_estacion` | Texto | Indica si el punto es estación o portal. |
| `x_pct` | Numérico | Coordenada horizontal aproximada. |
| `y_pct` | Numérico | Coordenada vertical aproximada. |
| `es_portal` | Numérico | Valor 1 si el punto es portal. |
| `posible_transbordo` | Numérico | Valor 1 si el punto puede funcionar como cambio o conexión. |
| `demanda_estimada` | Numérico | Demanda aproximada entre 0 y 100. |
| `demora_promedio_min` | Numérico | Demora promedio aproximada en minutos. |
| `frecuencia_buses_min` | Numérico | Frecuencia promedio estimada de buses. |

Este dataset no contiene una etiqueta objetivo. Por eso se usa para agrupar estaciones con características similares mediante aprendizaje no supervisado.

## Pruebas Ejecutadas

| Prueba | Comando | Explicación |
|---|---|---|
| 1 | `python main.py --generar-dataset` | Genera el dataset no supervisado que será usado por el modelo. |
| 2 | `python main.py --agrupar --clusters 3` | Agrupa las estaciones en 3 grupos y muestra la métrica `silhouette_score`. |
| 3 | `python main.py --predecir-grupo --clusters 3 --troncal "Suba" --tipo-estacion portal --es-portal 1 --posible-transbordo 1 --demanda 88 --demora 13 --frecuencia 4` | Asigna un caso nuevo al grupo más cercano usando 3 clusters. |
| 4 | `python main.py --predecir-grupo --clusters 3 --troncal "Calle 80" --tipo-estacion station --es-portal 0 --posible-transbordo 0 --demanda 42 --demora 4 --frecuencia 9` | Asigna otro caso nuevo al grupo más cercano usando 3 clusters. |
| 5 | `python main.py --agrupar --clusters 4` | Vuelve a ejecutar el agrupamiento, ahora con 4 grupos para comparar resultados. |
| 6 | `python main.py --predecir-grupo --clusters 4 --troncal "Caracas" --tipo-estacion station --es-portal 0 --posible-transbordo 1 --demanda 76 --demora 10 --frecuencia 6` | Asigna un caso nuevo al grupo más cercano usando 4 clusters. |
| 7 | `python main.py --predecir-grupo --clusters 4 --troncal "Américas" --tipo-estacion portal --es-portal 1 --posible-transbordo 1 --demanda 94 --demora 18 --frecuencia 3` | Asigna un segundo caso nuevo al grupo más cercano usando 4 clusters. |
