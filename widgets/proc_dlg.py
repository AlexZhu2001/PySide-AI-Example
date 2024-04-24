from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar


class ProcDlg(QWidget):
    def __init__(self, text: str, parent=None):
        assert parent is not None, "ProcDlg must have a parent"
        super().__init__(parent)
        self.setFixedSize(200, 100)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.text = QLabel(text, self)

        self.bar = QProgressBar(self)
        self.bar.setTextVisible(False)
        self.bar.setRange(0, 0)

        self.layout.addWidget(self.text, 0, Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.bar, 0, Qt.AlignmentFlag.AlignHCenter)

    def showEvent(self, e):
        self.move(
            (self.parentWidget().width() - self.width()) // 2,
            (self.parentWidget().height() - self.height()) // 2,
        )

    def paintEvent(self, event):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor(255, 255, 255, 125))
        super().paintEvent(event)
