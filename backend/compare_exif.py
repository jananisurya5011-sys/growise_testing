import json

with open('python_exif_results.json') as f:
    py_res = json.load(f)
with open('js_exif_results.json') as f:
    js_res = json.load(f)

print("--- EXIF ORIENTATION COMPARISON ---")
print(f"Python Shape: {py_res['python_shape']}")
print(f"JS Shape:     {js_res['js_shape']}")
print()
print(f"Python First Pixel: {py_res['python_first_pixel']}")
print(f"JS First Pixel:     {js_res['js_first_pixel']}")
print()
if py_res['python_shape'] != js_res['js_shape']:
    print("CONCLUSION: EXIF ORIENTATION IS HANDLED DIFFERENTLY!")
    print("Python (PIL) ignores EXIF rotation.")
    print("JavaScript (Browser) applies EXIF rotation.")
else:
    print("EXIF handling is identical.")
