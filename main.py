from os import remove, rename
from time import sleep
from typing import List, Tuple
from interface.camera.camera import savePicture
from net.train import printPredict2
from interface.motor.motor import left, right, middle

def difference(l1, l2) -> int:
    d = 0
    for [k, i] in enumerate(l1):
        if l2[k] > i + 7 or l2[k] < i - 7:
            d += 1
    return d

def makePicture(filename: str):
    savePicture("FHD Webcam", (384, 512), (0, 0, 350, 300), filename)

def readPicture(filename: str) -> List[int]:
    return open(filename, "rb").read()

CATEGORY_OPERATION = {
    "papier": left,
    "wertstof": right,
    "rest": middle
}

def mainLoop() -> bool:
    last2 = "../../last2.bmp"
    last = "../../last.bmp"
    makePicture(last2)
    
    while True:
        makePicture(last)
        lastImageBytes = readPicture(last2)
        currentImageBytes = readPicture(last)
        dif = difference(lastImageBytes, currentImageBytes)
        print(dif)
        if dif > 250_000:
            print("New item detected!")      
            category, score = printPredict2("/modelc5/5cv_200", last)
            # CATEGORY_OPERATION[category]()
            sleep(5)
            remove(last2)
            rename(last, last2)


mainLoop()