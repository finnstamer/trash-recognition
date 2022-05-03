# import matplotlib.pyplot as plt
from pydoc import classname
import numpy as np
import PIL.Image as Image
# import os
# import tensorflow as tf
import tensorflow as tf
from keras import layers
from keras.utils import conv_utils
# from tensorflow.keras import layers
from keras import Model

import pathlib

# Constants
image_height = 384
image_width = 512
relativeDataPath = "data"


data_dir = pathlib.Path(relativeDataPath)
normalization_layer = layers.Rescaling(1./255) # Normalizing RGB from 0-255 to 0-1

def getCategoryImages(category: str) -> list:
    return list(map(lambda x: str(x), data_dir.glob(f"{category}/*.jpg")))

def loadDataset(subset: str = "training") -> tf.data.Dataset:
    batchSize = 32 # Samples per training
    validationSplit = 0.2 # Proportion of data used for validation
    

    return tf.keras.utils.image_dataset_from_directory(
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
    return Model([
        layers.Rescaling(1./255, input_shape=(image_height, image_width, 3)),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(len(class_names))
    ])

# def compileModel(model: Model) -> Model:
#     model.compile(
#         optimizer="adam",
#         loss=tf.keras.losses(SparseCategoricalCrossentropy=)
#     )


train_ds = loadDataset()
val_ds = loadDataset("validation")
noramlized_train_ds = normalizeDataset(train_ds)

class_names = train_ds.class_names # Namen der Kategorien; korresponideren zu Ordnernamen in data_dir
model = createModel()
