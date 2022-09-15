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

def left():
    ROTATE = getRotationValue(1/4)
    setPos("1", ROTATE)
    start("1")

    sleep(2)
    setPos("1", - ROTATE)
    sleep(2)


def middle():
    ROTATE = 3/4 * _360
    setPos("1", ROTATE)
    # start("1")
    # sleep(2)
    # setPos("1", - ROTATE)


def middle():
    pass

def right():
    pass

sleep(2)
left()