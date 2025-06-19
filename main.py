import time
import numpy as np
import pyautogui
import mss
import os
import numpy as np

import main_model



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







# test_input = np.random.rand(144, 1, 3).astype(np.float32)
# predicted_label = infer(test_input)


# l = []

#     l.append(a)

# a = np.hstack(l)
# print(a.shape, a.min(), a.max())
# a = (a * 255).astype('uint8')
# iio.imwrite(os.path.join(PREFIX, 'res.png'), a)

# cptxsncd
# cptx..cd



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
