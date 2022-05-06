import numpy as np
from typing import Tuple
import tensorflow as tf
from pathlib import Path
from tensorflow.python.ops.nn import softmax
from keras.preprocessing.image import load_img, img_to_array
from tensorflow import expand_dims
from keras import layers
from tensorflow.python.keras.models import load_model
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

def augmentation() -> Sequential:
    return Sequential([
        layers.RandomFlip("horizontal_and_vertical", input_shape=(image_height, image_width, 3)),
        layers.RandomRotation(0.3),
        layers.RandomZoom(0.3),
    ])

def createModel(class_names) -> Model:
    return Sequential([
        augmentation(),
        layers.Rescaling(1./255, input_shape=(image_height, image_width, 3)),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.2),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
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

def predict(model: Model, imagePath: str) -> Tuple: # (category: str, confidence: float)
    img = load_img(imagePath, target_size=(image_height, image_width))
    imageArray = img_to_array(img)
    imageArray = expand_dims(imageArray, 0)
    
    predictions = model.predict(imageArray)
    score = softmax(predictions[0])
    category = class_names[np.argmax(score)]
    confidence = 100 * np.max(score)
    return (category, confidence)

def saveModel(model: Model, name: str):
    model.save(f"net/models/{name}")

def loadModel(name: str) -> Model:
    return load_model(f"net/models/{name}")

def AItrain(epochs=1) -> Tuple:
    train_ds = loadDataset()
    val_ds = loadDataset("validation")

    class_names = train_ds.class_names # Namen der Kategorien; korresponideren zu Ordnernamen in data_dir
    model = createModel(class_names)
    model = compileModel(model)
    history = train(model, train_ds, val_ds, epochs=epochs)
    return (model, history)

def printPredict(imagePath: str) -> Tuple:
    (category, score) = predict(model, imagePath)
    print(f"Classified image ({imagePath}) to be '{category}' wih {score}% confidence")
    return (category, score)


epochs = 300
(model, history) = AItrain(epochs)
# saveModel(model, "2")
# printPredict("path")
visualize(history, epochs, "Data Augmentation (hv-flip; rot0.3, zoo0.3) on 128 units and 0.2 dropout; 300 epochs")
