### Cell 0
```python
from google.colab import drive
drive.mount('/content/drive')
```

### Cell 1
```python
import os

drive_path = "/content/drive/MyDrive"

for root, dirs, files in os.walk(drive_path):
    for file in files:
        if file.endswith(".zip"):
            print(os.path.join(root, file))
```

### Cell 2
```python
import zipfile
import os

zip_path = "/content/drive/MyDrive/FinalDataset.zip"
extract_path = "/content/dataset"

os.makedirs(extract_path, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print("Dataset extracted successfully!")
```

### Cell 3
```python
import os

base = "/content/dataset/FinalDataset"

print("Folders:", os.listdir(base))
print()

print("Train classes:", len(os.listdir(base + "/train")))
print("Validation classes:", len(os.listdir(base + "/val")))
```

### Cell 4
```python
import os

base = "/content/dataset/FinalDataset"

print("Folders:", os.listdir(base))
print()

print("Train classes:", len(os.listdir(base + "/train")))
print("Validation classes:", len(os.listdir(base + "/val")))
```

### Cell 5
```python
import os

train_total = 0
val_total = 0

for c in os.listdir("/content/dataset/FinalDataset/train"):
    train_total += len(os.listdir(f"/content/dataset/FinalDataset/train/{c}"))

for c in os.listdir("/content/dataset/FinalDataset/val"):
    val_total += len(os.listdir(f"/content/dataset/FinalDataset/val/{c}"))

print("Training images :", train_total)
print("Validation images:", val_total)
```

### Cell 6
```python
!pip install -q tensorflow==2.15.0
```

### Cell 7
```python
!pip install -q tensorflow
```

### Cell 8
```python
import tensorflow as tf
print(tf.__version__)
```

### Cell 9
```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
```

### Cell 10
```python
import tensorflow as tf
print("TensorFlow:", tf.__version__)
print("Python:", __import__("sys").version)
```

### Cell 11
```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

train_dir = "/content/dataset/FinalDataset/train"
val_dir = "/content/dataset/FinalDataset/val"

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(
    rescale=1./255
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)
```

### Cell 12
```python
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model

base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224,224,3)
)

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
output = Dense(train_generator.num_classes, activation="softmax")(x)

model = Model(base_model.input, output)

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()
```

### Cell 13
```python
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10
)
```

### Cell 14
```python
import tensorflow as tf
print(tf.config.list_physical_devices("GPU"))
```

### Cell 15
```python
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

train_dir = "/content/dataset/FinalDataset/train"
val_dir = "/content/dataset/FinalDataset/val"

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

validation_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)
```

### Cell 16
```python
from google.colab import drive
drive.mount('/content/drive')
```

### Cell 17
```python
import zipfile
import os

zip_path = "/content/drive/MyDrive/FinalDataset.zip"
extract_path = "/content/dataset"

os.makedirs(extract_path, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print("Dataset extracted successfully!")
```

### Cell 18
```python
import os

print(os.listdir("/content/dataset"))
```

### Cell 19
```python
print(os.listdir("/content/dataset/FinalDataset"))
```

### Cell 20
```python
len(os.listdir("/content/dataset/FinalDataset/train"))
```

### Cell 21
```python
train_dir = "/content/dataset/FinalDataset/train"
val_dir = "/content/dataset/FinalDataset/val"
```

### Cell 22
```python
import os

zip_path = "/content/drive/MyDrive/FinalDataset.zip"
print("Exists:", os.path.exists(zip_path))
print("Size (GB):", os.path.getsize(zip_path) / (1024**3))
```

### Cell 23
```python
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

train_dir = "/content/dataset/FinalDataset/train"
val_dir = "/content/dataset/FinalDataset/val"

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

validation_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)
```

### Cell 24
```python
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model

base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224,224,3)
)

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)

predictions = Dense(
    train_generator.num_classes,
    activation="softmax"
)(x)

model = Model(base_model.input, predictions)
```

### Cell 25
```python
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
```

### Cell 26
```python
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=10
)
```

### Cell 27
```python
base_model.trainable = True

# Freeze the first layers
for layer in base_model.layers[:-30]:
    layer.trainable = False
```

### Cell 28
```python
from tensorflow.keras.optimizers import Adam

model.compile(
    optimizer=Adam(learning_rate=1e-5),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
```

### Cell 29
```python
history_finetune = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=10
)
```

### Cell 30
```python
model.save("/content/drive/MyDrive/GroWise_Model.keras")
```

### Cell 31
```python
loss, accuracy = model.evaluate(validation_generator)

print("Validation Loss:", loss)
print("Validation Accuracy:", accuracy)
```

### Cell 32
```python
import matplotlib.pyplot as plt

acc = history.history['accuracy'] + history_finetune.history['accuracy']
val_acc = history.history['val_accuracy'] + history_finetune.history['val_accuracy']

loss = history.history['loss'] + history_finetune.history['loss']
val_loss = history.history['val_loss'] + history_finetune.history['val_loss']

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(acc)
plt.plot(val_acc)
plt.title("Accuracy")
plt.legend(["Train","Validation"])

plt.subplot(1,2,2)
plt.plot(loss)
plt.plot(val_loss)
plt.title("Loss")
plt.legend(["Train","Validation"])

plt.show()
```

### Cell 33
```python
validation_generator.reset()

predictions = model.predict(validation_generator)
```

### Cell 34
```python
import numpy as np
from sklearn.metrics import classification_report

y_pred = np.argmax(predictions, axis=1)

print(classification_report(
    validation_generator.classes,
    y_pred,
    target_names=list(validation_generator.class_indices.keys())
))
```

### Cell 35
```python
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

cm = confusion_matrix(validation_generator.classes, y_pred)

plt.figure(figsize=(15,15))
sns.heatmap(cm, cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()
```

### Cell 36
```python
model.save("/content/drive/MyDrive/GroWise_Model.keras")
```

### Cell 37
```python
print(train_generator.class_indices)
print(train_generator.num_classes)
```

### Cell 38
```python
from google.colab import drive
drive.mount('/content/drive')
```

### Cell 39
```python
import os

print(os.listdir("/content/drive/MyDrive"))
```

### Cell 40
```python
import os

print(os.path.exists("/content/drive/MyDrive/FinalDataset.zip"))
```

### Cell 41
```python
import zipfile

zip_path = "/content/drive/MyDrive/FinalDataset.zip"
extract_path = "/content/dataset"

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(extract_path)
```

### Cell 42
```python
import os

print(os.listdir("/content/dataset"))
print(os.listdir("/content/dataset/FinalDataset"))
```

### Cell 43
```python
classes = os.listdir("/content/dataset/FinalDataset/train")

print(classes)
print("Number of classes:", len(classes))
```

### Cell 44
```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMG_SIZE = (224,224)
BATCH_SIZE = 32

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(
    rescale=1./255
)

train_generator = train_datagen.flow_from_directory(
    "/content/dataset/FinalDataset/train",
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

validation_generator = val_datagen.flow_from_directory(
    "/content/dataset/FinalDataset/val",
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)
```

### Cell 45
```python
import json

class_indices = train_generator.class_indices

with open("/content/drive/MyDrive/class_indices.json", "w") as f:
    json.dump(class_indices, f, indent=4)

print(class_indices)
```

### Cell 46
```python
from google.colab import drive
drive.mount('/content/drive')
```

### Cell 47
```python
import os

os.path.exists("/content/drive/MyDrive/GroWise_Model.keras")
```

### Cell 48
```python
import tensorflow as tf

model = tf.keras.models.load_model("/content/drive/MyDrive/GroWise_Model.keras")

converter = tf.lite.TFLiteConverter.from_keras_model(model)

tflite_model = converter.convert()

with open("/content/drive/MyDrive/crop_model.tflite","wb") as f:
    f.write(tflite_model)

print("DONE")
```

