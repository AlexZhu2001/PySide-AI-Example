import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QResource
from widgets.main_window import MainWindow
from widgets.except_dlg import ExceptionDialog
from core.global_exc import init_except, ExceptHooks
from core.signal_handler import handler


def closeAll(*args, **kwargs):
    QApplication.closeAllWindows()


def main(argv: list[str]):
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.RoundPreferFloor
    )
    app = QApplication(argv)

    QResource.registerResource("./resources.bin")

    init_except(False)
    ExceptHooks.register(ExceptionDialog.handleException)
    ExceptHooks.register(closeAll)

    handler.connect_qt_app(app)

    w = MainWindow()
    w.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
