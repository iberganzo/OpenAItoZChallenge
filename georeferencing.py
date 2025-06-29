import os
import rasterio
import geopandas as gpd
from shapely.geometry import Point

# 3x3
region_map = {
    "NW": (0, 0), "N": (1, 0), "NE": (2, 0),
    "W":  (0, 1), "C": (1, 1), "E":  (2, 1),
    "SW": (0, 2), "S": (1, 2), "SE": (2, 2)
}

entries = []
with open('potential_sites_detected.txt') as f:
    for line in f:
        if ';' in line:
            name_part, region = line.strip().split(';')
            name = os.path.splitext(name_part)[0]
            entries.append((name, region))

points = []

for name, region in entries:
    tif_path = f'work_dataset_evi/crops_tif/{name}.tif'

    if not os.path.exists(tif_path):
        print(f"File not found: {tif_path}")
        continue

    with rasterio.open(tif_path) as src:
        if region not in region_map:
            region = "C"
        col, row = region_map[region]
        cell_w = src.width / 3
        cell_h = src.height / 3

        center_x = (col + 0.5) * cell_w
        center_y = (row + 0.5) * cell_h

        lon, lat = src.transform * (center_x, center_y)
        points.append({'geometry': Point(lon, lat), 'name': name})

gdf = gpd.GeoDataFrame(points, crs=src.crs)

# WGS84 (EPSG:4326)
if gdf.crs.to_epsg() != 4326:
    gdf = gdf.to_crs(epsg=4326)

# Guardar shapefile
gdf.to_file('potential_sites_detected.shp')
print("End Of Line")
