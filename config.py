import os
import time
import pyautogui

PREFIX = os.path.dirname(__file__)
REFERENCE_FILENAMES = ['ptcd.png', 'xwpw.png', 'pcsn.png']

LETTERS = "cptxsnwd" # coin, pile, trefle, 2x, snake, net, croWn, dash
NAMES = dict(
    c= 'coin',
    p= 'pile',
    t= 'tref',
    x= '2x--',
    s= 'snak',
    n= 'net-',
    w= 'crown',
    d= 'dash',
)


def CLICK():
    time.sleep(0.01)
    pyautogui.mouseDown()
    time.sleep(0.01)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.mouseUp()
    time.sleep(0.01)

class machine5spin:
    CLICK_LEVER = lambda: (pyautogui.moveTo(3280, 930, duration=0.5), CLICK(), CLICK())
    CLICK_B0 = lambda: (pyautogui.moveTo(1468, 1487, duration=0.5), CLICK(), CLICK())
    CLICK_B1 = lambda: (pyautogui.moveTo(1768, 1487, duration=0.5), CLICK(), CLICK())
    CLICK_B2 = lambda: (pyautogui.moveTo(2090, 1487, duration=0.5), CLICK(), CLICK())
    CLICK_B3 = lambda: (pyautogui.moveTo(2386, 1487, duration=0.5), CLICK(), CLICK())
    Y0, Y1 = 1019, 1163
    XS = [1464, 1763, 2068, 2357]
    SPIN_Y = 1490
    SPIN_XS = [2645, 2705, 2765, 2828, 2887]
    DELTA = 20
    SPIN_COUNT = 5

class machine3spin:
    CLICK_LEVER = lambda: (pyautogui.moveTo(3280, 930, duration=0.5), CLICK(), CLICK())
    CLICK_B0 = lambda: (pyautogui.moveTo(1670, 1420, duration=0.5), CLICK(), CLICK())
    CLICK_B1 = lambda: (pyautogui.moveTo(1943, 1420, duration=0.5), CLICK(), CLICK())
    CLICK_B2 = lambda: (pyautogui.moveTo(2236, 1420, duration=0.5), CLICK(), CLICK())
    CLICK_B3 = lambda: (pyautogui.moveTo(2519, 1420, duration=0.5), CLICK(), CLICK())
    Y0, Y1 = 1019 - 43, 1163 - 43
    XS = [
        2357 + 139 - 278 - 295 - 278,
        2357 + 139 - 278 - 295,
        2357 + 139 - 278,
        2357 + 139,
    ]
    SPIN_Y = 1420
    SPIN_XS = [2768, 2850, 2939]
    DELTA = 20
    SPIN_COUNT = 3

# MACHINE = machine5spin
MACHINE = machine3spin

MSS_SCREEN_ID = 2
SCREEN_W = 3840
SCREEN_H = 2160
