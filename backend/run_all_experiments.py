import json
import numpy as np
from PIL import Image
import tensorflow as tf
import inspect
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# 1. Prove Keras default
sig = inspect.signature(ImageDataGenerator.flow_from_directory)
default_interp = sig.parameters['interpolation'].default
print("="*50)
print(f"PROVEN: ImageDataGenerator.flow_from_directory default interpolation is '{default_interp}'")
print("="*50)

def load_json_tensor(path, key):
    with open(path, 'r') as f:
        data = json.load(f)
    return np.array(data[key], dtype=np.float32).reshape((1, 224, 224, 3))

def get_python_tensor(image_path, resample_method):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224), resample=resample_method)
    return np.array(img, dtype=np.float32) / 255.0
    
image_path = r'C:\Projects\GroWise_Fullstack\GroWise\backend\uploads\crop\dis2.jpg'
py_bicubic_tensor = get_python_tensor(image_path, Image.Resampling.BICUBIC)
py_bilinear_tensor = get_python_tensor(image_path, Image.Resampling.BILINEAR)
py_nearest_tensor = get_python_tensor(image_path, Image.Resampling.NEAREST)

# Expand dims
py_bicubic_tensor = np.expand_dims(py_bicubic_tensor, axis=0)
py_bilinear_tensor = np.expand_dims(py_bilinear_tensor, axis=0)
py_nearest_tensor = np.expand_dims(py_nearest_tensor, axis=0)

js_bilinear_tensor = load_json_tensor(r'C:\Projects\GroWise_Fullstack\GroWise\backend\dis2_js_results.json', 'js_full_tensor')
js_nearest_tensor = load_json_tensor(r'C:\Projects\GroWise_Fullstack\GroWise\backend\dis2_js_nearest.json', 'js_full_tensor')

# Load TFLite Model
interpreter = tf.lite.Interpreter(model_path=r'C:\Projects\GroWise_Fullstack\GroWise\website\public\ml\crop_model.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def run_inference(tensor):
    interpreter.set_tensor(input_details[0]['index'], tensor)
    interpreter.invoke()
    return interpreter.get_tensor(output_details[0]['index'])[0]

res_py_bicubic = run_inference(py_bicubic_tensor)
res_py_bilinear = run_inference(py_bilinear_tensor)
res_py_nearest = run_inference(py_nearest_tensor)
res_js_bilinear = run_inference(js_bilinear_tensor)
res_js_nearest = run_inference(js_nearest_tensor)

experiments = {
    'A': ('Python BICUBIC', res_py_bicubic),
    'B': ('Python BILINEAR', res_py_bilinear),
    'C': ('Python NEAREST', res_py_nearest),
    'D': ('JavaScript BILINEAR', res_js_bilinear),
    'E': ('JavaScript NEAREST', res_js_nearest)
}

with open(r'C:\Projects\GroWise_Fullstack\GroWise\backend\models\class_indices.json', 'r') as f:
    classes_raw = json.load(f)
    classes = {int(v): k for k, v in classes_raw.items()}

# Print experiment results
print("### 4. Controlled Experiments\n")
for key, (name, probs) in experiments.items():
    pred_idx = np.argmax(probs)
    conf = np.max(probs)
    top5 = np.argsort(probs)[-5:][::-1]
    print(f"**Experiment {key}: {name}**")
    print(f"- **Predicted Class:** {classes[pred_idx]}")
    print(f"- **Predicted Index:** {pred_idx}")
    print(f"- **Confidence:** {conf:.6f}")
    print(f"- **Top 5 Predictions:** {[(int(i), classes[i], float(probs[i])) for i in top5]}")
    print(f"- **Raw 39-class output vector:** `[{', '.join([f'{p:.4f}' for p in probs])}]`\n")

# Compare raw logits
def compare_probs(p1, p2, name):
    diff = np.abs(p1 - p2)
    max_diff = np.max(diff)
    mean_diff = np.mean(diff)
    rmse = np.sqrt(np.mean(diff**2))
    print(f"**{name}**")
    print(f"- Maximum Absolute Difference: {max_diff:.6f}")
    print(f"- Mean Absolute Difference: {mean_diff:.6f}")
    print(f"- RMSE: {rmse:.6f}\n")

print("### 6. Compare Raw Logits\n")
compare_probs(res_py_bicubic, res_js_bilinear, "Python (Bicubic) vs JavaScript (Bilinear) [Current Production Mismatch]")
compare_probs(res_py_nearest, res_js_nearest, "Python (Nearest) vs JavaScript (Nearest) [Theoretical Unified Pipeline]")
compare_probs(res_py_bilinear, res_js_bilinear, "Python (Bilinear) vs JavaScript (Bilinear)")

