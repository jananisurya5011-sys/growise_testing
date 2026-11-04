import json
import numpy as np
from PIL import Image

image_path = r'C:\Projects\GroWise_Fullstack\GroWise\backend\uploads\crop\dis2.jpg'
img = Image.open(image_path).convert('RGB')

# Python actually uses BICUBIC because it omits the resample param!
img_bicubic = img.resize((224, 224), resample=Image.Resampling.BICUBIC)
arr_bicubic = np.array(img_bicubic, dtype=np.float32) / 255.0

results = {
    'python_bicubic_first_100': arr_bicubic.flatten()[:100].tolist(),
    'python_bicubic_full': arr_bicubic.flatten().tolist(),
    'shape': list(arr_bicubic.shape),
    'dtype': str(arr_bicubic.dtype)
}

with open(r'C:\Projects\GroWise_Fullstack\GroWise\backend\dis2_python_bicubic.json', 'w') as f:
    json.dump(results, f)

print("Python bicubic dumped.")
