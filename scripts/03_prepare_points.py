"""
Convierte los CSV de coordenadas de inundaciones a GeoJSON.

Entradas:
  data/raw/puntos_entrenamiento.csv  (coordenadas usadas para entrenar el modelo)
  data/raw/puntos_validacion.csv     (coordenadas usadas para validar el modelo)

Salidas:
  web/data/puntos_entrenamiento.geojson
  web/data/puntos_validacion.geojson

Los CSV están en EPSG:32613 (UTM Zona 13N) con columnas coord_x y coord_y.
El GeoJSON se guarda en EPSG:4326 (WGS84) — estándar requerido por GeoJSON.
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd

ARCHIVOS = [
    ("data/raw/puntos_entrenamiento.csv", "web/data/puntos_entrenamiento.geojson"),
    ("data/raw/puntos_validacion.csv", "web/data/puntos_validacion.geojson"),
]

COL_X = "coord_x"
COL_Y = "coord_y"
CRS_ORIGEN = "EPSG:32613"
CRS_SALIDA = "EPSG:4326"


def preparar_puntos(input_path: str, output_path: str) -> None:
    entrada = Path(input_path)
    salida = Path(output_path)
    salida.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(entrada)
    print(f"\n{entrada.name}")
    print(f"  Registros: {len(df)}")
    print(f"  Columnas:  {list(df.columns)}")

    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df[COL_X], df[COL_Y]),
        crs=CRS_ORIGEN,
    )

    gdf = gdf.to_crs(CRS_SALIDA)

    gdf.to_file(salida, driver="GeoJSON")
    print(f"  -> GeoJSON guardado en: {salida} (reproyectado a {CRS_SALIDA})")


if __name__ == "__main__":
    for input_path, output_path in ARCHIVOS:
        preparar_puntos(input_path, output_path)
