import time
import numpy as np
import pyautogui
import mss
import imageio.v3 as iio

a = iio.imread(r'\\wsl$\Ubuntu-18.04\home\nico\test\405\baseline.png')
assert a.shape == (2160, 3840, 3)
assert a.dtype.name == 'uint8'
a = (a.astype('float32') / 255.).mean(axis=-1)
assert a.shape == (2160, 3840)

print(a.shape, a.dtype)

def CLICK():
    time.sleep(0.01)
    pyautogui.mouseDown()
    time.sleep(0.01)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.mouseUp()
    time.sleep(0.01)

CLICK_LEVER = lambda: (pyautogui.moveTo(3280, 930, duration=0.5), CLICK(), CLICK())
CLICK_B0 = lambda: (pyautogui.moveTo(1468, 1487, duration=0.5), CLICK(), CLICK())
CLICK_B1 = lambda: (pyautogui.moveTo(1768, 1487, duration=0.5), CLICK(), CLICK())
CLICK_B2 = lambda: (pyautogui.moveTo(2090, 1487, duration=0.5), CLICK(), CLICK())
CLICK_B3 = lambda: (pyautogui.moveTo(2386, 1487, duration=0.5), CLICK(), CLICK())




# print('coucou')
# with mss.mss() as sct:
#     monitor = sct.monitors[2]
#     img = sct.grab(monitor)
#     img = np.asarray(img)[:, :, [2, 1, 0]]
#     print('  Snapshoted!', img.shape)
#     assert img.shape == (2160, 3840, 3)


# CLICK_LEVER()
# time.sleep(3)
# CLICK_B0()
# time.sleep(3)
# CLICK_B1()
# time.sleep(3)
# CLICK_B2()
# time.sleep(3)
# CLICK_B3()

# for _ in range(10):
    # CLICK_LEVER()
    # time.sleep(1)
    # CLICK()
    # pyautogui.click()
    # print('clicked')


# CLICK_LEVER()

# pyautogui.click()






#
