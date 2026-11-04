import json
import numpy as np

with open(r'C:\Projects\GroWise_Fullstack\GroWise\backend\dis2_python_tensor.json', 'r') as f:
    py = json.load(f)

with open(r'C:\Projects\GroWise_Fullstack\GroWise\backend\dis2_js_results.json', 'r') as f:
    js = json.load(f)

py_flat = np.array(py['python_first_100'])
js_flat = np.array(js['js_first_100'])

diff = np.abs(py_flat - js_flat)
max_err = diff.max()
mae = diff.mean()
rmse = np.sqrt(np.mean(diff**2))

print("TENSOR DIFFERENCES:")
print(f"Max Absolute Error: {max_err:.6f}")
print(f"Mean Absolute Error: {mae:.6f}")
print(f"RMSE: {rmse:.6f}")

print("\nPROBABILITIES DIFFERENCES:")
py_probs = np.array(js['probs_py'])
js_probs = np.array(js['probs_js'])

for i in range(len(py_probs)):
    print(f"Index {i:2d} | Python: {py_probs[i]:.6f} | JS: {js_probs[i]:.6f} | Diff: {abs(py_probs[i] - js_probs[i]):.6f}")

print("\nPYTHON PREDICTION:", np.argmax(py_probs), "Confidence:", np.max(py_probs))
print("JS PREDICTION:    ", np.argmax(js_probs), "Confidence:", np.max(js_probs))
