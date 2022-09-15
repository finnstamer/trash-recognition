from typing import Tuple
from pygame import camera, image
from time import sleep

def getCamera(cam: str, size: Tuple):
    camera.init()
    cam = camera.Camera(cam, size)
    cam.start()
    sleep(1)
    return cam
    
def savePicture(cam: str, size: Tuple, saveFile: str) -> None:
    img = getCamera(cam, size).get_image()
    image.save(img, saveFile, "jpg")

# savePicture("FHD Webcam", (384, 512), "../../test.bmp")
# newItem("FHD Webcam", (512, 384))
