import os
import json
import numpy as np
from PIL import Image

# 1. Create a synthetic test image (e.g. 500x500 gradient with noise, mimicking a high-res photo)
width, height = 500, 500
image_data = np.zeros((height, width, 3), dtype=np.uint8)
for y in range(height):
    for x in range(width):
        image_data[y, x, 0] = (x + y) % 256
        image_data[y, x, 1] = (x * y) % 256
        image_data[y, x, 2] = int(127.5 + 127.5 * np.sin(x/10.0) * np.cos(y/10.0))

img = Image.fromarray(image_data, 'RGB')
img.save('test_image.png')

# 2. Simulate Keras Python preprocessing
# image.load_img(..., target_size=(224,224)) uses PIL.Image.resize with interpolation='nearest' by default in Keras 2.x / 3.x
# We will test both NEAREST and BILINEAR in PIL to show the differences.

# Python Nearest (Default)
img_nearest = img.resize((224, 224), resample=Image.Resampling.NEAREST)
arr_nearest = np.array(img_nearest, dtype=np.float32) / 255.0

# Python Bilinear
img_bilinear = img.resize((224, 224), resample=Image.Resampling.BILINEAR)
arr_bilinear = np.array(img_bilinear, dtype=np.float32) / 255.0

# Extract first 100 floats (flat)
flat_nearest = arr_nearest.flatten()[:100].tolist()
flat_bilinear = arr_bilinear.flatten()[:100].tolist()

results = {
    'python_nearest_first_100': flat_nearest,
    'python_bilinear_first_100': flat_bilinear,
    'shape': list(arr_nearest.shape),
    'dtype': str(arr_nearest.dtype),
    'min': float(arr_nearest.min()),
    'max': float(arr_nearest.max()),
    'mean': float(arr_nearest.mean())
}

with open('python_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("Python preprocessing complete. Results saved.")
