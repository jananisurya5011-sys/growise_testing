from PIL import Image
print("PIL VERSION:", getattr(Image, '__version__', 'unknown'))
import inspect
print(inspect.signature(Image.Image.resize))
