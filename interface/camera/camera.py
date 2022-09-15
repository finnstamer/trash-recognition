from typing import Tuple
from pygame import camera, image
def savePicture(cam: str, dimensions: Tuple, saveFile: str) -> None:
    camera.init()
    print(camera.list_cameras())
    cam = camera.Camera(cam, dimensions)
    cam.start()
    img = cam.get_image()
    image.save(img, saveFile)