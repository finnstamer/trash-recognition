from tkinter import MOVETO
from pyautogui import moveTo, leftClick, position, typewrite, press
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

def backspace():
    press("BACKSPACE", 20)

def setPos(motor: str, value: int):
    moveTo(TARGET_POS[motor])
    leftClick()
    backspace()
    print(str(value))
    typewrite(str(value))

def start(motor: str):
    moveTo(REL[motor])
    leftClick()

def stop(motor: str):
    moveTo(STOP[motor])
    leftClick()

_360 = 52_000.00
def left():
    ROTATE = 1.00/4.00 * _360
    print(1/4, 1/4 * _360)
    setPos("1", ROTATE)
    start("1")
    sleep(2)
    setPos("1", - ROTATE)


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

# sleep(2)
# setPos("1", 10_000)
# start("1")
# # start("2")
left()