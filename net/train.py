import tensorflow as tf
from pathlib import Path
from keras import layers
from keras import Sequential, Model
from keras.preprocessing.image_dataset import image_dataset_from_directory
from keras.losses import SparseCategoricalCrossentropy
from visualize import visualize

# Constants
image_height = 384
image_width = 512


data_dir = Path("net/data") # Why net/ if this file is already in net???
normalization_layer = layers.Rescaling(1./255) # Normalizing RGB from 0-255 to 0-1

def getCategoryImages(category: str) -> list:
    return list(map(lambda x: str(x), data_dir.glob(f"{category}/*.jpg")))

def loadDataset(subset: str = "training") -> tf.data.Dataset:
    batchSize = 32 # Samples per training
    validationSplit = 0.2 # Proportion of data used for validation
    

    return image_dataset_from_directory(
        data_dir,
        validation_split=validationSplit,
        subset=subset,
        seed=123,
        image_size=(image_height, image_width),
        batch_size=batchSize
    )

def normalizeDataset(ds: tf.data.Dataset) -> tf.data.Dataset:
    return ds.map(lambda x, y: (normalization_layer(x), y))

def createModel(class_names) -> Model:
    return Sequential([
        layers.Rescaling(1./255, input_shape=(image_height, image_width, 3)),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.2), # new
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        # layers.Dense(48, activation='relu'),
        layers.Dense(len(class_names))
    ])

def compileModel(model: Model) -> Model:
    model.compile(
        optimizer="adam",
        loss=SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    return model

def train(model: Model, train_ds: tf.data.Dataset, validation_ds: tf.data.Dataset, epochs: int=10):
    history = model.fit(
        train_ds,
        validation_data=validation_ds,
        epochs=epochs
    )
    return history

# trash = getCategoryImages("*")
# print(len(trash))
train_ds = loadDataset()
val_ds = loadDataset("validation")
noramlized_train_ds = normalizeDataset(train_ds)

class_names = train_ds.class_names # Namen der Kategorien; korresponideren zu Ordnernamen in data_dir
model = createModel(class_names)
model = compileModel(model)
history = train(model, train_ds, val_ds)
visualize(history, 10, "overfitting_64_less units and 0.2dropout")