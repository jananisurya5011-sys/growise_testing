from PIL import Image
print(Image.Resampling.BICUBIC)
img = Image.new('RGB', (100, 100))
img2 = img.resize((50, 50))
print("Did it crash? No.")
