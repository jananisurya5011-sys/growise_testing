import numpy as np
import json

python_tensor = np.load(r'C:\Projects\GroWise_Fullstack\GroWise\backend\python_input.npy').flatten()

with open(r'C:\Projects\GroWise_Fullstack\GroWise\backend\js_resize_variants.json', 'r') as f:
    js_data = json.load(f)

print("Comparing Python Pillow (NEAREST) to TensorFlow.js variants:")

best_rmse = float('inf')
best_variant = None

for key, val in js_data.items():
    js_tensor = np.array(val, dtype=np.float32)
    diff = np.abs(python_tensor - js_tensor)
    mae = np.mean(diff)
    max_err = np.max(diff)
    rmse = np.sqrt(np.mean(diff**2))
    print(f"\nVariant: {key}")
    print(f"Max Error: {max_err:.8f}")
    print(f"RMSE:      {rmse:.8f}")
    if rmse < best_rmse:
        best_rmse = rmse
        best_variant = key

print(f"\nBest match: {best_variant} with RMSE = {best_rmse:.8f}")
