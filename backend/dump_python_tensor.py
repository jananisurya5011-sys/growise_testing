import json
import numpy as np
from PIL import Image

image_path = r'C:\Projects\GroWise_Fullstack\GroWise\backend\uploads\crop\dis2.jpg'
img = Image.open(image_path).convert('RGB')

# Keras flow_from_directory and load_img default is nearest
img_nearest = img.resize((224, 224), resample=Image.Resampling.NEAREST)
arr_nearest = np.array(img_nearest, dtype=np.float32) / 255.0

# Extract first 100 floats
flat_nearest = arr_nearest.flatten()[:100].tolist()

results = {
    'python_first_100': flat_nearest,
    'shape': list(arr_nearest.shape),
    'dtype': str(arr_nearest.dtype),
    'min': float(arr_nearest.min()),
    'max': float(arr_nearest.max()),
    'mean': float(arr_nearest.mean()),
    'full_tensor': arr_nearest.flatten().tolist()
}

with open(r'C:\Projects\GroWise_Fullstack\GroWise\backend\dis2_python_tensor.json', 'w') as f:
    json.dump(results, f)

print("Python tensor dumped.")
