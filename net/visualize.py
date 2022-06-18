import matplotlib.pyplot as plt
from time import strftime
from random import randrange

def visualize(history, epochs: int, name: str):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    timestr = strftime("%Y%m%d-%H%M%S")
    plt.suptitle(name, fontsize=14)
    path = f"results/{timestr}.png"
    plt.savefig(path)

def vis_augmentation(set, augmentation_func, num, name="test data augmentation"):
    plt.figure(figsize=(10, 10))
    aug = augmentation_func()
    for images, _ in set.shuffle(200).take(1):
        plt.subplot(3, 3, 1)
        plt.imshow(images[0].numpy().astype("uint8"))
        plt.title("Original", fontsize=32)
        plt.axis("off")
        for i in range(1, num):
            plt.subplot(3, 3, i + 1)
            augmented_images = aug(images)
            plt.imshow(augmented_images[0].numpy().astype("uint8"))
            plt.axis("off")
        path = f"results/data-aug/{name}-{num}.png"
        plt.savefig(path)
