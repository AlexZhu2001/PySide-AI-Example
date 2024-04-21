import sys
from PySide6.QtWidgets import QApplication
from widgets.main_window import MainWindow


def main(argv: list[str]):
    app = QApplication(argv)
    w = MainWindow()
    w.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
