import signal
from types import FrameType

from PySide6.QtWidgets import QApplication


class SignalHandler:
    def __init__(self):
        self.app = None  # type: QApplication | None

    def handler(self, sig: int, _: FrameType | None):
        if sig != 2:
            return
        if self.app is not None:
            self.app.closeAllWindows()

    def register_all(self):
        signal.signal(signal.SIGINT, self.handler)

    def connect_qt_app(self, app: QApplication):
        self.app = app


handler = SignalHandler()
handler.register_all()
