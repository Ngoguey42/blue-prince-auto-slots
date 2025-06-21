import imageio.v3 as iio
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from config import *
import matplotlib.pyplot as plt



"""
y in 1019:1163

1464 1019
1763 1019
2068 1020
2357 1020
"""



def peek(img, i, plot, m=MACHINE):
    assert img.shape == (SCREEN_H, SCREEN_W, 3)
    assert img.dtype.name == 'float32'
    assert i in [0, 1, 2, 3]
    x = m.XS[i]
    a = img[m.Y0:m.Y1, x-m.DELTA:x+1+m.DELTA]

    if plot:
        plt.close('all')
        plt.imshow(a)
        plt.show()
        plt.close('all')

    assert 0 <= a.min() <= a.max() <= 1.0
    a = np.median(a, axis=1)
    a = a[:, None, :]
    assert a.shape == (m.Y1 - m.Y0, 1, 3)
    return a

needles = {}
for filename in REFERENCE_FILENAMES:
    path = os.path.join(PREFIX, filename)
    print(path)
    img = iio.imread(path)
    print(img.shape)
    assert img.shape == (SCREEN_H, SCREEN_W, 3)
    assert img.dtype.name == 'uint8'
    img = (img.astype('float32') / 255.)
    assert img.shape == (SCREEN_H, SCREEN_W, 3)
    assert 0 <= img.min() < img.max() <= 1.0
    print(img.shape, img.dtype)

    for i, letter in enumerate(filename[:4]):
        if letter in needles: continue
        print(f'  peek {letter=:}')
        a = peek(img, i, plot=False, m=machine5spin)


        needles[letter] = a
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
