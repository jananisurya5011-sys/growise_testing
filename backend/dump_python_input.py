import numpy as np
from PIL import Image

def get_python_tensor(image_path):
    target_size = (224, 224)
    img = Image.open(image_path).convert('RGB')
    img = img.resize(target_size, resample=Image.Resampling.NEAREST)
    img_array = np.array(img, dtype=np.float32)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

image_path = r'C:\Projects\GroWise_Fullstack\GroWise\backend\uploads\crop\dis2.jpg'
tensor = get_python_tensor(image_path)
np.save(r'C:\Projects\GroWise_Fullstack\GroWise\backend\python_input.npy', tensor)
print(f"Python input saved, shape: {tensor.shape}, min: {tensor.min()}, max: {tensor.max()}")
