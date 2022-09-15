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
# from visualize import vis_augmentation, visualize, visualize_
# Constants
image_height = 384
image_width = 512


data_dir = Path("net/data")
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
        layers.RandomRotation(1),
        layers.RandomZoom(0.2),
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
        layers.Conv2D(128, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(128, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
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
    Path("models").mkdir(False, exist_ok=True)
    model.save(f"models/{name}")

def loadModel(name: str) -> Model:
    return load_model(f"net/models/{name}")

def AItrain(epochs=1) -> Tuple:
    train_ds = loadDataset()
    val_ds = loadDataset("validation")

    global class_names
    class_names = train_ds.class_names # Namen der Kategorien; korresponideren zu Ordnernamen in data_dir
    model = createModel(class_names)
    model = compileModel(model)
    history = train(model, train_ds, val_ds, epochs=epochs)
    return (model, history)

def printPredict(model: Model, imagePath: str) -> Tuple:
    (category, score) = predict(model, imagePath)
    print(f"Classified image ({imagePath}) to be '{category}' with conf: {score}")
    return (category, score)


def trainMultiple(epochs, name):
    t_ds = loadDataset()
    v_ds = loadDataset("validation")
    class_names = t_ds.class_names
    model = createModel(class_names)
    model = compileModel(model)
    trained_epochs = 0
    for _epochs in epochs:
        print(f"Now training for {_epochs} epochs.")
        history = train(model, t_ds, v_ds, _epochs)
        trained_epochs += _epochs
        saveModel(model, f"{name}_{trained_epochs}")
        visualize(history, _epochs, f"data-Aug (r:1, z=0.2, f=hv); 5cv(16*x) 128fc [{trained_epochs - _epochs}-{trained_epochs}]", name)

# trainMultiple([2, 3], "test")
# trainMultiple([25, 25, 25, 25, 25, 25, 25, 25], "5cv")


# epochs = 20
# (model, history) = AItrain(epochs)
# visualize(history, epochs, "data-Aug (r:1, z=0.2, f=hv); 5cv(16*x) 128fc")
# saveModel(model, "3")
# Next more or less cv's
def printPredict2(model: str, file: str):
    train_ds = loadDataset()
    global class_names
    class_names = train_ds.class_names
    model = loadModel(model) # modelc5/5cv_200
    (category, score) = predict(model, file)
    if score < 98:
        print(f"Nicht erkannt. ({category}:{score})")
    else:
        print(f"{category}:{score}%")