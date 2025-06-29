import os
import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio.transform import Affine
from PIL import Image

# Example for the EVI imagery
input_tif_path = 'work_dataset_evi.tif' # Replace with your EVI and NDRE imagery TIF names
tile_name = os.path.splitext(os.path.basename(input_tif_path))[0]

crop_size = 128
visual_min = 0.5
visual_max = 0.75

out_dir_tif = 'work_dataset_evi/crops_tif' # Select your output folders for TIF and JPG
out_dir_jpg = 'work_dataset_evi/crops_jpg'
os.makedirs(out_dir_tif, exist_ok=True)
os.makedirs(out_dir_jpg, exist_ok=True)

def normalize_band(band, vmin, vmax):
    norm = (band - vmin) / (vmax - vmin)
    norm = np.clip(norm, 0, 1)
    return (norm * 255).astype(np.uint8)

with rasterio.open(input_tif_path) as src:
    width = src.width
    height = src.height
    count = src.count  # number of bands
    crs = src.crs
    transform = src.transform
    dtype = src.dtypes[0]
    print(f"Original shape: ({height}, {width}, {count}) CRS: {crs}")

    for y in range(0, height, crop_size):
        for x in range(0, width, crop_size):
            win = Window(x, y, crop_size, crop_size)
            crop = src.read(window=win)  # shape: (bands, H, W)

            # === Save GeoTIFF crop ===
            transform_crop = rasterio.windows.transform(win, transform)
            tif_crop_path = os.path.join(out_dir_tif, f"{tile_name}_crop_{y}_{x}.tif")

            profile = src.profile.copy()
            profile.update({
                'height': crop.shape[1],
                'width': crop.shape[2],
                'transform': transform_crop
            })

            with rasterio.open(tif_crop_path, 'w', **profile) as dst:
                dst.write(crop)

            # === Prepare RGB visualization ===
            band1 = crop[0].astype(np.float32)
            band2 = crop[1].astype(np.float32)
            r = normalize_band(band1, visual_min, visual_max)
            g = normalize_band(band2, visual_min, visual_max)
            b = normalize_band((band1 + band2) / 2, visual_min, visual_max)
            rgb = np.stack([r, g, b], axis=-1)

            jpg_crop_path = os.path.join(out_dir_jpg, f"{tile_name}_crop_{y}_{x}.jpg")
            Image.fromarray(rgb, mode='RGB').save(jpg_crop_path, quality=90)

print("All crops saved with georeferencing and JPG.")

