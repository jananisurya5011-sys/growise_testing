import json
import numpy as np

with open(r'C:\Projects\GroWise_Fullstack\GroWise\backend\dis2_python_bicubic.json', 'r') as f:
    py = json.load(f)

with open(r'C:\Projects\GroWise_Fullstack\GroWise\backend\dis2_js_results.json', 'r') as f:
    js = json.load(f)

py_flat = np.array(py['python_bicubic_full'])
js_flat = np.array(js['js_full_tensor'])

diff = np.abs(py_flat - js_flat)
max_err = float(diff.max())
mae = float(diff.mean())
rmse = float(np.sqrt(np.mean(diff**2)))

print("--- BICUBIC (Python) vs BILINEAR (JS) TENSOR DIFFERENCES ---")
print(f"Max Absolute Error: {max_err:.6f}")
print(f"Mean Absolute Error: {mae:.6f}")
print(f"RMSE: {rmse:.6f}")

print("\nFirst 10 values:")
print("Python BICUBIC:", [round(x, 4) for x in py['python_bicubic_first_100'][:10]])
print("JS BILINEAR:   ", [round(x, 4) for x in js['js_first_100'][:10]])
