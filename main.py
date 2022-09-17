from copy import copy
from os import remove, rename
from shutil import copy as shutil_copy
import shutil
from time import sleep
from typing import List, Tuple
from interface.camera.camera import savePicture, fillWithBlank
from net.train import printPredict2
from interface.motor.motor import left, right, middle

def difference(l1, l2) -> int:
    d = 0
    for [k, i] in enumerate(l1):
        if l2[k] > i + 5 or l2[k] < i - 5:
            d += 1
    return d

def makePicture(filename: str):
    savePicture("FHD Webcam", (512, 384), saveFile=filename)
    # fillWithBlank(filename, (60, 96, 255, 209), filename, (255, 255, 255), negative=True)


def readPicture(filename: str) -> List[int]:
    return open(filename, "rb").read()

CATEGORY_OPERATION = {
    "papier": left,
    "wertstof": right,
    "rest": middle
}

SCORE_TRESHHOLD = 97.00
def mainLoop(lastImageNumber = 31) -> bool:
    last2 = "../../last2.bmp"
    last = "../../last.bmp"
    makePicture(last2)

    while True:
        makePicture(last)
        lastImageBytes = readPicture(last2)
        currentImageBytes = readPicture(last)
        changed_bytes = difference(lastImageBytes, currentImageBytes)
        print(changed_bytes)
        if changed_bytes > 120_000:
            print("New item detected!")      
            category, score = printPredict2("/modelc5/5cv_200", last)
            if score >= SCORE_TRESHHOLD:
                CATEGORY_OPERATION[category]()
                shutil_copy(last, f"real_images/{lastImageNumber}.bmp")
                remove(last2)
                rename(last, last2)
                sleep(5)
                # mainLoop(lastImageNumber+1) # Verhindere, dass das verschwundene Item als new item gewertet wird, indem ein neues vergleichsbild (last2) gemacht wird
                break;
        sleep(5)


mainLoop()
