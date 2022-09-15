from typing import Tuple
from interface.camera.camera import savePicture
from net.train import printPredict2
def difference(l1, l2) -> int:
    d = 0
    for [k, i] in enumerate(l1):
        if l2[k] > i + 5 or l2[k] < i - 5:
            d += 1
    return d

# savePicture("FHD Webcam", (384, 512), "../../last.jpg")
def mainLoop(cam: str, size: Tuple) -> bool:
    savePicture("FHD Webcam", (384, 512), "../../last2.bmp")
    while True:
        savePicture(cam, size, "../../last.bmp")
        lastImageBytes = open("../../last2.bmp", "rb").read()
        currentImageBytes = open("../../last.bmp", "rb").read()
        dif = difference(lastImageBytes, currentImageBytes)
        print(dif)
        if dif > 250_000:
            print("New item detected!")            
            printPredict2("/modelc5/5cv_200", "../../last.bmp")
            savePicture(cam, size, "../../last2.bmp")

mainLoop("FHD Webcam", (384, 512))