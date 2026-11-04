import os
import json
import numpy as np
from PIL import Image

# Create a 200 (width) x 100 (height) image with a gradient
width, height = 200, 100
image_data = np.zeros((height, width, 3), dtype=np.uint8)
for y in range(height):
    for x in range(width):
        image_data[y, x, 0] = x
        image_data[y, x, 1] = y
        image_data[y, x, 2] = 128

img = Image.fromarray(image_data, 'RGB')

# Save with EXIF orientation = 6 (Rotated 90 CW)
# EXIF tag 274 is Orientation. 6 means "Rotate 90 CW".
# We use piexif to add EXIF.
import piexif
exif_dict = {"0th": {piexif.ImageIFD.Orientation: 6}}
exif_bytes = piexif.dump(exif_dict)
img.save('test_exif.jpg', "jpeg", exif=exif_bytes)

print("Saved test_exif.jpg with EXIF Orientation = 6 (Rotate 90 CW)")

# Now load using Keras's underlying logic (PIL without exif_transpose)
# keras.utils.load_img uses PIL.Image.open
img_loaded = Image.open('test_exif.jpg')
img_loaded = img_loaded.convert('RGB')
arr_loaded = np.array(img_loaded)

results = {
    'python_shape': list(arr_loaded.shape),
    'python_first_pixel': arr_loaded[0, 0].tolist(),
    'python_last_pixel': arr_loaded[-1, -1].tolist()
}

with open('python_exif_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("Python EXIF test complete.")
