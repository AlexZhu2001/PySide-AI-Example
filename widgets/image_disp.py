from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QImage, QPainter
from PySide6.QtCore import Qt, QSize, QPoint, QRect

class ImageDisp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._img = QImage()

    def set_image(self, img: QImage):
        self._img = img

    def calc_rect(self):
        if self._img.isNull():
            return QRect()
        wr = self.rect()
        ir = self._img.rect()
        ws = wr.width() / ir.width()
        hs = wr.height() / ir.height()
        scale = min(ws, hs)
        size = QSize(int(ir.width() * scale), int(ir.height() * scale))
        pos = QPoint((wr.width() - size.width()) // 2,
                     (wr.height() - size.height()) // 2)
        return QRect(pos, size)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHints(
            QPainter.Antialiasing |
            QPainter.TextAntialiasing |
            QPainter.SmoothPixmapTransform |
            QPainter.LosslessImageRendering
        )
        p.fillRect(self.rect(), Qt.transparent)
        p.drawImage(self.calc_rect(), self._img)
