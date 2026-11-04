import json
import numpy as np

with open('python_results.json') as f:
    py_res = json.load(f)
with open('js_results.json') as f:
    js_res = json.load(f)

py_nearest = np.array(py_res['python_nearest_first_100'])
py_bilinear = np.array(py_res['python_bilinear_first_100'])
js_bilinear = np.array(js_res['js_bilinear_first_100'])
js_nearest = np.array(js_res['js_nearest_first_100'])

def compare(arr1, arr2, name):
    diff = np.abs(arr1 - arr2)
    max_err = diff.max()
    mae = diff.mean()
    rmse = np.sqrt(np.mean(diff**2))
    print(f"--- {name} ---")
    print(f"Max Absolute Error: {max_err:.6f}")
    print(f"Mean Absolute Error: {mae:.6f}")
    print(f"RMSE: {rmse:.6f}")
    print()

print("SHAPE AND DTYPE COMPARISON")
print(f"Python Shape: {py_res['shape']}, Dtype: {py_res['dtype']}")
print(f"JS Shape: {js_res['shape']}, Dtype: {js_res['dtype']}")
print()

compare(py_nearest, js_bilinear, "Python Nearest (Default) vs JS Bilinear (Current)")
compare(py_bilinear, js_bilinear, "Python Bilinear vs JS Bilinear")
compare(py_nearest, js_nearest, "Python Nearest vs JS Nearest")

print("--- Sample First 10 Floats ---")
print("Python Nearest:", [round(x, 4) for x in py_nearest[:10]])
print("JS Bilinear:   ", [round(x, 4) for x in js_bilinear[:10]])
print("JS Nearest:    ", [round(x, 4) for x in js_nearest[:10]])
