import inspect
import keras.preprocessing.image as img_prep

sig = inspect.signature(img_prep.ImageDataGenerator.flow_from_directory)
print("ImageDataGenerator.flow_from_directory default interpolation:")
print(sig.parameters['interpolation'].default)
