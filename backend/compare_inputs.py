import numpy as np
import json

python_tensor = np.load(r'C:\Projects\GroWise_Fullstack\GroWise\backend\python_input.npy')

with open(r'C:\Projects\GroWise_Fullstack\GroWise\backend\js_input.json', 'r') as f:
    js_data = json.load(f)
js_tensor = np.array(js_data['values'], dtype=np.float32).reshape(js_data['shape'])

print("=== Python Input ===")
print("Shape:", python_tensor.shape)
print("Dtype:", python_tensor.dtype)
print("Min:", np.min(python_tensor))
print("Max:", np.max(python_tensor))
print("Mean:", np.mean(python_tensor))
print("Std:", np.std(python_tensor))
print("First 10 values:", python_tensor.flatten()[:10])
print("Last 10 values:", python_tensor.flatten()[-10:])

print("\n=== JS Input ===")
print("Shape:", js_tensor.shape)
print("Dtype:", js_tensor.dtype)
print("Min:", np.min(js_tensor))
print("Max:", np.max(js_tensor))
print("Mean:", np.mean(js_tensor))
print("Std:", np.std(js_tensor))
print("First 10 values:", js_tensor.flatten()[:10])
print("Last 10 values:", js_tensor.flatten()[-10:])

diff = np.abs(python_tensor - js_tensor)
mae = np.mean(diff)
max_err = np.max(diff)
rmse = np.sqrt(np.mean(diff**2))

print("\n=== Comparison ===")
print(f"Maximum Absolute Error: {max_err:.8f}")
print(f"Mean Absolute Error: {mae:.8f}")
print(f"RMSE: {rmse:.8f}")
