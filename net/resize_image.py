from glob import glob
from typing import Tuple
from PIL import Image


def resizeImage(image: Image.Image, size: Tuple):
    return image.resize(size, 1)


def filesInFolder(dir: str):
    return glob(f"{dir}/*.*")


def resizeImages(dir: str, size: Tuple, output_dir: str, output_name_prefix = ""):
    files = filesInFolder(dir)
    for f in files:
        imageName = f.split("\\")[-1]
        image = Image.open(f)
        image = resizeImage(image, size)
        image.save(f"{output_dir}/{output_name_prefix}{imageName}")
    