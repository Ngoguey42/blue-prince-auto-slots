import imageio.v3 as iio
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


PREFIX = os.path.dirname(__file__)



"""
y in 1019:1163

1464 1019
1763 1019
2068 1020
2357 1020
"""


LETTERS = "cptxsncd" # coin, pile, trefle, 2x, snake, net, crown, dash
Y0, Y1 = 1019, 1163
XS = [1464, 1763, 2068, 2357]
DELTA = 20

def peek(img, i):
    assert img.shape == (2160, 3840, 3)
    assert img.dtype.name == 'float32'
    assert i in [0, 1, 2, 3]
    x = XS[i]
    a = img[Y0:Y1, x-DELTA:x+1+DELTA]
    assert 0 <= a.min() < a.max() <= 1.
    a = np.median(a, axis=1)
    a = a[:, None, :]
    assert a.shape == (Y1 - Y0, 1, 3)
    return a

filenames = ['ptcd.png', 'xcpc.png', 'pcsn.png']
needles = {}
for filename in filenames:
    path = os.path.join(PREFIX, filename)
    print(path)
    img = iio.imread(path)
    print(img.shape)
    assert img.shape == (2160, 3840, 3)
    assert img.dtype.name == 'uint8'
    img = (img.astype('float32') / 255.)
    assert img.shape == (2160, 3840, 3)
    assert 0 <= img.min() < img.max() <= 255
    print(img.shape, img.dtype)

    for i, letter in enumerate(filename[:4]):
        if letter in needles: continue
        a = peek(img, i)
        # x = XS[i]
        # a = img[Y0:Y1, x-DELTA:x+1+DELTA]
        # print('slice', a.shape)
        # a = np.median(a, axis=1)
        # print('slice', a.shape)
        # a = a[:, None, :]
        # print('slice', a.shape)
        # print()
        needles[letter] = a
        # print(f'{needles[letter].shape=:}')
assert set(LETTERS) == set(needles.keys())

X = []
y = []
for label, arr in needles.items():
    X.append(arr.flatten())  # Flatten to shape (432,)
    y.append(label)

X = np.array(X)
y = np.array(y)

knn = KNeighborsClassifier(n_neighbors=1)  # 1-NN since you have only one sample per class
knn.fit(X, y)

def infer(input_array: np.ndarray) -> str:
    assert input_array.shape == (144, 1, 3), "Input shape must be (144, 1, 3)"
    assert input_array.dtype == np.float32, "Input dtype must be float32"
    flattened = input_array.flatten().reshape(1, -1)
    return knn.predict(flattened)[0]

for k, a in needles.items():
    k2 = infer(a)
    assert k == k2


#
