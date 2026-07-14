# Mapa de Susceptibilidad a Inundaciones — AMG

Mapa interactivo de susceptibilidad a inundaciones para el Área Metropolitana de Guadalajara.

## Estructura del proyecto

```
mapa-inundaciones-gdl/
├── scripts/
│   ├── 01_reproject_raster.py   # EPSG:32613 → EPSG:3857
│   ├── 02_generate_tiles.py     # raster → tiles PNG para el mapa
│   └── 03_prepare_points.py     # CSV → GeoJSON (puntos de inundación)
├── web/
│   ├── index.html               # página del mapa
│   ├── tiles/                   # generado por script (no en git)
│   └── data/                    # GeoJSON de puntos
└── data/
    └── raw/                     # rasters originales (no en git)
```

## Setup

```bash
pip install rasterio numpy Pillow mercantile geopandas
```

## Flujo de trabajo

### 1. Coloca los archivos fuente

```
data/raw/raster_clasificado.tif      ← raster con valores 1-5
data/raw/puntos_entrenamiento.csv    ← coordenadas de entrenamiento
data/raw/puntos_validacion.csv       ← coordenadas de validación
```

### 2. Ejecuta los scripts en orden

```bash
python scripts/01_reproject_raster.py    # reproyecta a EPSG:3857
python scripts/02_generate_tiles.py      # genera los tiles del mapa
python scripts/03_prepare_points.py      # convierte CSV a GeoJSON
```

### 3. Ajusta las URLs de descarga en web/index.html

Busca el bloque `const DOWNLOADS` y reemplaza los links con los de
GitHub Releases (raster 111 MB) y Zenodo (raster entrenamiento 1 GB).

### 4. Prueba localmente

```bash
# Desde la carpeta web/
python -m http.server 8000
# Abre http://localhost:8000
```

### 5. Despliega en GitHub Pages

Sube el contenido de `web/` a la rama `gh-pages` del repositorio.

## Paleta de colores

| Clase | Susceptibilidad | Color    |
|-------|----------------|----------|
| 1     | Muy baja       | #1a9641  |
| 2     | Baja           | #a6d96a  |
| 3     | Moderada       | #ffffbf  |
| 4     | Alta           | #fdae61  |
| 5     | Muy alta       | #d7191c  |
