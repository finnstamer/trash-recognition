from typing import Tuple
from pygame import camera, image
from time import sleep
from PIL import Image as PILImage

def getCamera(cam: str, size: Tuple):
    camera.init()
    cam = camera.Camera(cam, size)
    cam.start()
    sleep(1)
    return cam
    
def savePicture(cam: str, size: Tuple, crop: Tuple, saveFile: str) -> None:
    img = getCamera(cam, size).get_image()
    image.save(img, saveFile, "bmp")
    img = PILImage.open(saveFile)
    img_cropped = img.crop(crop)
    img_cropped.save(saveFile, "bmp")