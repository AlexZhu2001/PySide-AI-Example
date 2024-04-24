import traceback

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont, QPainter, QColor
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSizePolicy, QPushButton


class ExceptionDialog(QDialog):
    def __init__(self, exc_class: type, exc_obj: object, tb_obj, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip)
        self.exc_class = exc_class
        self.exc_obj = exc_obj
        self.tb_obj = tb_obj

        self.layout = QVBoxLayout(self)

        self.label = QLabel(self.tr("An unexpected error occurred, Program will exit!"), self)
        f = QFont()
        f.setPointSizeF(15)
        self.label.setFont(f)

        self.btn = QPushButton(self.tr("Exit program"), self)
        self.btn.clicked.connect(self.accept)

        self.info = QLabel(self)
        self._make_info()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.info)
        self.layout.addWidget(self.btn)

    def _make_info(self):
        text = [
                   f"Error Name:       {self.exc_class.__name__}",
                   f"Error object id:   0x{id(self.exc_obj):X}",
               ] + traceback.extract_tb(self.tb_obj).format()
        self.info.setText("\n".join(text))

    @classmethod
    def handleException(cls, exc_class, exc_obj, tb_obj):
        dlg = cls(exc_class, exc_obj, tb_obj)
        dlg.exec()

    def paintEvent(self, event):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor(0x66, 0xcc, 0xff, 120))
        super().paintEvent(event)
