"""
Genera tiles PNG (formato XYZ) a partir del raster clasificado en EPSG:3857.
Entrada:  data/raster_3857.tif
Salida:   docs/tiles/{z}/{x}/{y}.png

Paleta de colores:
  1 = Muy bajo     ->verde fuerte  (#1a9641)
  2 = Bajo         ->verde claro   (#a6d96a)
  3 = Moderado     ->amarillo      (#ffffbf)
  4 = Alto         ->naranja       (#fdae61)
  5 = Muy alto     ->rojo          (#d7191c)
  0 = NoData       ->transparente
"""

from pathlib import Path

import mercantile
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.transform import from_bounds
from rasterio.warp import reproject
from PIL import Image

INPUT = Path("data/raster_3857.tif")
OUTPUT_DIR = Path("docs/tiles")
ZOOM_MIN = 10
ZOOM_MAX = 14
TILE_SIZE = 256

COLORMAP = {
    1: (26, 150, 65, 220),    # verde fuerte
    2: (166, 217, 106, 220),  # verde claro
    3: (255, 255, 191, 220),  # amarillo
    4: (253, 174, 97, 220),   # naranja
    5: (215, 25, 28, 220),    # rojo
}


def aplicar_colores(data: np.ndarray) -> np.ndarray:
    rgba = np.zeros((TILE_SIZE, TILE_SIZE, 4), dtype=np.uint8)
    for valor, color in COLORMAP.items():
        mask = data == valor
        rgba[mask] = color
    return rgba


def generar_tile(src, tile: mercantile.Tile) -> Image.Image | None:
    bounds = mercantile.xy_bounds(tile)

    tile_transform = from_bounds(
        bounds.left, bounds.bottom, bounds.right, bounds.top,
        TILE_SIZE, TILE_SIZE,
    )

    data = np.zeros((TILE_SIZE, TILE_SIZE), dtype=np.uint8)

    try:
        reproject(
            source=rasterio.band(src, 1),
            destination=data,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=tile_transform,
            dst_crs="EPSG:3857",
            resampling=Resampling.nearest,
        )
    except Exception:
        return None

    if data.max() == 0:
        return None

    rgba = aplicar_colores(data)
    return Image.fromarray(rgba, "RGBA")


def generar_tiles():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with rasterio.open(INPUT) as src:
        bounds_4326 = rasterio.warp.transform_bounds(
            src.crs, "EPSG:4326", *src.bounds
        )
        west, south, east, north = bounds_4326
        print(f"Extensión (WGS84): {west:.4f}, {south:.4f}, {east:.4f}, {north:.4f}")

        for zoom in range(ZOOM_MIN, ZOOM_MAX + 1):
            tiles = list(mercantile.tiles(west, south, east, north, zooms=zoom))
            print(f"Zoom {zoom}: {len(tiles)} tiles")

            generadas = 0
            for tile in tiles:
                img = generar_tile(src, tile)
                if img is None:
                    continue

                ruta = OUTPUT_DIR / str(tile.z) / str(tile.x)
                ruta.mkdir(parents=True, exist_ok=True)
                img.save(ruta / f"{tile.y}.png", "PNG")
                generadas += 1

            print(f"  ->{generadas} tiles con datos guardadas")

    print(f"\nTiles generadas en: {OUTPUT_DIR}")


if __name__ == "__main__":
    generar_tiles()
