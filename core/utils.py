import cv2
import numpy as np
from PySide6.QtGui import QImage


def qimage_to_mat(img: QImage):
    img = img.convertToFormat(QImage.Format_ARGB32)
    width, height, depth = img.width(), img.height(), img.depth() // 8
    ptr = img.constBits()
    sz = height * width * depth
    ptr = ptr[:sz]
    mat = np.frombuffer(ptr, np.uint8).reshape(
        (height, width, depth)
    )
    mat = cv2.cvtColor(mat, cv2.COLOR_RGBA2RGB)
    return mat
