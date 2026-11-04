import os
import sys
import hashlib
import numpy as np
from PIL import Image

# Import TensorFlow
try:
    import tensorflow as tf
except ImportError:
    print("TensorFlow is required to run this script. Please install it.")
    sys.exit(1)

def get_preprocessed_tensor(image_path):
    target_size = (224, 224)
    # EXACT preprocessing steps specified
    # 1. PIL Image.open()
    img = Image.open(image_path)
    # 2. convert("RGB")
    img = img.convert('RGB')
    # 3. resize(224,224) - Using NEAREST as per previous fix, but sticking to default if specified.
    # The instructions just said resize(224,224). We'll use NEAREST as that was the proven fix.
    img = img.resize(target_size, resample=Image.Resampling.NEAREST)
    # 4. float32
    img_array = np.array(img, dtype=np.float32)
    # 5. divide by 255
    img_array = img_array / 255.0
    # 6. expand dims
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def run_keras_inference(model_path, tensor):
    model = tf.keras.models.load_model(model_path)
    probs = model.predict(tensor, verbose=0)[0]
    return probs

def run_tflite_inference(model_path, tensor):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    interpreter.set_tensor(input_details[0]['index'], tensor)
    interpreter.invoke()
    
    probs = interpreter.get_tensor(output_details[0]['index'])[0]
    return probs

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, 'ai_engine', 'models')
    
    keras_path = os.path.join(models_dir, 'GroWise_Model.keras')
    tflite_path = os.path.join(base_dir, '..', 'website', 'public', 'ml', 'crop_model.tflite')
    
    # Fallback to local tflite if not found in website folder
    if not os.path.exists(tflite_path):
        tflite_path = os.path.join(models_dir, 'crop_model.tflite')
        
    image_path = os.path.join(base_dir, 'uploads', 'crop', 'dis2.jpg')
    
    if not os.path.exists(keras_path):
        print(f"Keras model not found at {keras_path}")
        return
    if not os.path.exists(tflite_path):
        print(f"TFLite model not found at {tflite_path}")
        return
    if not os.path.exists(image_path):
        print(f"Image not found at {image_path}")
        return

    print("Loading models and preparing tensor...")
    tensor = get_preprocessed_tensor(image_path)
    
    # Print first 20 input floats
    print("\n--- Tensor Details ---")
    print(f"First 20 input floats:\n{tensor.flatten()[:20]}")
    
    # Print tensor SHA256
    tensor_bytes = tensor.tobytes()
    tensor_hash = hashlib.sha256(tensor_bytes).hexdigest()
    print(f"Input tensor SHA256: {tensor_hash}")
    
    print("\n--- Running Keras Inference ---")
    keras_probs = run_keras_inference(keras_path, tensor)
    keras_argmax = int(np.argmax(keras_probs))
    keras_conf = float(keras_probs[keras_argmax])
    
    print(f"Keras probabilities (first 10): {keras_probs[:10]}")
    print(f"Keras argmax: {keras_argmax}")
    print(f"Keras confidence: {keras_conf:.6f}")
    
    print("\n--- Running TFLite Inference ---")
    tflite_probs = run_tflite_inference(tflite_path, tensor)
    tflite_argmax = int(np.argmax(tflite_probs))
    tflite_conf = float(tflite_probs[tflite_argmax])
    
    print(f"TFLite probabilities (first 10): {tflite_probs[:10]}")
    print(f"TFLite argmax: {tflite_argmax}")
    print(f"TFLite confidence: {tflite_conf:.6f}")
    
    print("\n--- Comparison ---")
    diff = np.abs(keras_probs - tflite_probs)
    max_diff = np.max(diff)
    mean_diff = np.mean(diff)
    rmse = np.sqrt(np.mean(diff**2))
    
    print(f"Max absolute difference: {max_diff:.8e}")
    print(f"Mean difference: {mean_diff:.8e}")
    print(f"RMSE: {rmse:.8e}")
    
    print("\n--- Final Verdict ---")
    if keras_argmax != tflite_argmax:
        print("KERAS AND TFLITE ARE DIFFERENT")
    else:
        print("KERAS AND TFLITE MATCH")

if __name__ == "__main__":
    main()
