from pyautogui import moveTo, leftClick, position, typewrite, keyDown
from time import sleep
TARGET_POS_1 = (896, 420)
STOP_1 = (896, 525)
REL_START_1 = (767, 520)

STOP_2 = (1406, 525)
TARGET_POS_2 = (1406, 420)
REL_START_2 = (1280, 520)

def backspace():
    for i in range(25):
        keyDown("BACKSPACE")

def setREL1(value: int):
    moveTo(TARGET_POS_1)
    leftClick()
    backspace()
    typewrite(str(value))


sleep(2)
setREL1(50)