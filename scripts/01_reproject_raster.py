"""
Reproyecta el raster de EPSG:32613 a EPSG:3857 (Web Mercator).
Entrada:  data/raw/raster_clasificado.tif  (valores 1-5, EPSG:32613)
Salida:   data/raster_3857.tif             (mismo valores, EPSG:3857)
"""

from pathlib import Path

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject

INPUT = Path("data/raw/raster_clasificado.tif")
OUTPUT = Path("data/raster_3857.tif")

DST_CRS = "EPSG:3857"


def reproyectar():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with rasterio.open(INPUT) as src:
        print(f"CRS origen:    {src.crs}")
        print(f"Dimensiones:   {src.width} x {src.height}")
        print(f"Valores únicos: {np.unique(src.read(1))}")

        transform, width, height = calculate_default_transform(
            src.crs, DST_CRS, src.width, src.height, *src.bounds
        )

        kwargs = src.meta.copy()
        kwargs.update(
            crs=DST_CRS,
            transform=transform,
            width=width,
            height=height,
            nodata=0,  # -9999 del origen se convierte a 0 → transparente en tiles
        )

        with rasterio.open(OUTPUT, "w", **kwargs) as dst:
            reproject(
                source=rasterio.band(src, 1),
                destination=rasterio.band(dst, 1),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=DST_CRS,
                resampling=Resampling.nearest,
            )

    print(f"Raster reproyectado guardado en: {OUTPUT}")


if __name__ == "__main__":
    reproyectar()
