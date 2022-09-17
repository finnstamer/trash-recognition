from symbol import factor
from tkinter import MOVETO
from pyautogui import moveTo, leftClick, position, typewrite, press, keyDown
from time import sleep

STOP = {
    "1": (896, 525),
    "2": (1406, 525)
}
TARGET_POS = {
    "1": (896, 420),
    "2": (1406, 420)
}

REL = {
    "1": (767, 520),
    "2": (1280, 520)
}

EMERGENCY_STOP = (44, 128)

def printCursorPos():
    while True:
        print(position())
def backspace(times=1):
    press("BACKSPACE", times)

def setText(text: str, maxContentLen=20):
    backspace(maxContentLen)
    typewrite(text)

def setPos(motor: str, value: int):
    moveTo(TARGET_POS[motor])
    leftClick()
    backspace()
    setText(str(value))

def start(motor: str):
    moveTo(REL[motor])
    leftClick()

def stop(motor: str):
    moveTo(STOP[motor])
    leftClick()

def emergencyStop():
    moveTo(EMERGENCY_STOP)
    leftClick()

_360 = 52_000
def getRotationValue(factorOfFullRot: float) -> int:
    return int(factorOfFullRot * _360)

def firstLeft():
    setPos("1", -2200)
    start("1")

    sleep(2)

    setPos("1", 2200)
    start("1")
    sleep(2)

def firstRight():
    setPos("1", 600)
    start("1")
    sleep(2)
    setPos("1", -500)
    start("1")
    sleep(2)

def secondRight():
    setPos("2", -900)
    start("2")
    sleep(2)
    setPos("2", 1100)
    start("2")
    sleep(2)


def secondLeft():
    setPos("2", 800)
    start("2")
    sleep(2)
    setPos("2", -1000)
    start("2")
    sleep(2)

def left():
    firstLeft()

def middle():
    firstRight()
    secondLeft()

def right():
    firstRight()
    secondRight()

if __name__ == '__main__':
    # right()
    middle()
# sleep(2)
# left()