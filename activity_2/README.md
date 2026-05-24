<h1 align="center">🔥 Actividad 2 🧑‍💻</h1>
<h2 align="center">🔥 Búsqueda y sistemas basados en reglas🧑‍💻</h2>
<h3 align="center">Sistema inteligente de rutas para TransMilenio Bogotá</h3>

## Introducción

Este proyecto implementa en Python un sistema inteligente basado en reglas lógicas para calcular una ruta entre un punto A y un punto B del sistema TransMilenio de Bogotá. La solución se ejecuta únicamente desde la terminal, porque el propósito de esta actividad es demostrar el procedimiento del sistema inteligente, sobre la base de conocimiento, el motor de inferencia y los algoritmos de búsqueda.

## Representación del problema

El sistema de transporte se representa como un grafo:

- Cada estación o portal es un nodo.
- Cada conexión entre estaciones es una arista con costo.
- Las reglas lógicas construyen la base de conocimiento.
- El motor de inferencia aplica algoritmos de búsqueda para retornar la mejor ruta.

## Base de conocimiento

| Regla lógica | Representación |
|---|---|
| **R1** | **SI** dos estaciones pertenecen a la misma troncal y son consecutivas, **ENTONCES** se conectan en ambos sentidos con costo de desplazamiento. |
| **R2** | **SI** dos estaciones tienen nombre equivalente o pertenecen al mismo punto de intercambio, **ENTONCES** se agrega una conexión de transbordo con penalización baja. |
| **R3** | **SI** dos estaciones de troncales distintas están muy cerca en el mapa, **ENTONCES** se agrega una conexión peatonal de intercambio. |
| **R4** | **SI** existe origen, destino y algoritmo de búsqueda, **ENTONCES** el motor de inferencia retorna la mejor secuencia de estaciones. |
| **R5** | **SI** el algoritmo seleccionado es A*, **ENTONCES** se usa una heurística basada en la distancia aproximada entre estaciones. |

## Algoritmos Implementados

| Algoritmo | Tipo de búsqueda | Descripción |
|---|---|---|
| `astar` | Búsqueda informada | Algoritmo A*, recomendado para la entrega porque usa costo acumulado y heurística. |
| `dijkstra` | Búsqueda de costo uniforme | Calcula la ruta con menor costo acumulado entre el origen y el destino. |
| `bfs` | Búsqueda no informada | Búsqueda en anchura; explora primero los nodos más cercanos por niveles. |
| `dfs` | Búsqueda no informada | Búsqueda en profundidad; explora un camino hasta el fondo antes de retroceder. |

## Requisitos

| Lenguaje de Programación | Versión |
|---|---|
| Python | 3.13.x o superior |

## Instalación

| Sistema Operativo | Nombre del comando | Comando |
|---|---|---|
| Windows | Navegar Carpeta | `cd activity_2` |
| Windows | Entorno Virtual | `python -m venv .venv` |
| Windows | Activar Entorno | `.venv\Scripts\activate` |
| Windows | Verificar Entorno | `python -m site` |
| Windows | Instalar Dependencias | `pip install -r requirements.txt` |

| Sistema Operativo | Nombre del comando | Comando |
|---|---|---|
| Linux o macOS | Navegar Carpeta | `cd activity_2` |
| Linux o macOS | Entorno Virtual | `python -m venv .venv` |
| Linux o macOS | Activar Entorno | `source .venv/bin/activate` |
| Linux o macOS | Verificar Entorno | `python -m site` |
| Linux o macOS | Instalar Dependencias | `pip install -r requirements.txt` |

## Ejecución Terminal

Sobre la terminal navegar hasta la carpeta `activity_2` para ejecutar los comandos necesarios:

| Algoritmo | Ejemplo | Comando |
|---|---|---|
| `dijkstra` | `Portal Suba` a `Portal Américas` | `python main.py --origen "Portal Suba" --destino "Portal Américas" --algoritmo dijkstra` |
| `astar`    | `Portal Suba` a `Portal Américas` | `python main.py --origen "Portal Suba" --destino "Portal Américas" --algoritmo astar`    |
| `bfs`      | `Portal Suba` a `Portal Américas` | `python main.py --origen "Portal Suba" --destino "Portal Américas" --algoritmo bfs`      |
| `dfs`      | `Portal Suba` a `Portal Américas` | `python main.py --origen "Portal Suba" --destino "Portal Américas" --algoritmo dfs`      |

## Guias

| Ayuda | Comando |
|---|---|
| Estaciones Disponibles | `python main.py --listar-estaciones` |
| Reglas Locgicas | `python main.py --ver-reglas` |

## Estructura Organizada

```txt
activity_2/
├── data/
│   └── transmilenio.json
├── models/
│   ├── __init__.py
│   └── route_models.py
├── services/
│   ├── __init__.py
│   ├── inference_engine.py
│   ├── knowledge_base.py
│   ├── search_algorithms.py
│   └── text_utils.py
├── main.py
├── README.md
└── requirements.txt
```

## Procedimiento del sistema inteligente

1. El usuario ingresa la estación origen, la estación destino y el algoritmo.
2. El programa carga el archivo de datos `transmilenio.json`.
3. La base de conocimiento transforma las estaciones en nodos y conexiones.
4. Las reglas lógicas generan relaciones entre estaciones consecutivas, transbordos y conexiones cercanas.
5. El motor de inferencia consulta la base de conocimiento.
6. El algoritmo de búsqueda calcula la ruta.
7. El programa imprime el resultado en formato JSON.
