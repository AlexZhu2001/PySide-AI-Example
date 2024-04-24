from PySide6.QtWidgets import QMainWindow, QFileDialog, QApplication
from PySide6.QtCore import QDir, Slot
from PySide6.QtGui import QImage, QIcon

from core.classes import CLASSES
from ui.main_window import Ui_MainWindow
from core.model import WorkerThread, Models
from core.utils import qimage_to_mat
from .proc_dlg import ProcDlg
from .settings import Settings

IMAGE_FILTER = """
All Image Files (*.bmp *.ico *.gif *.jpeg *.jpg *.png *.tif *.tiff);;
Windows Bitmap (*.bmp);;
Windows Icon (*.ico);;
Graphics Interchange Format (*.gif);;
JPEG File Interchange Format (*.jpg *.jpeg);;
Portable Network Graphics (*.png);;
Tag Image File Format (*.tif *tiff);;
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.img = QImage()
        self.worker = None  # type: WorkerThread|None

        self.proc_dlg = ProcDlg("Calculating...", self)
        self.proc_dlg.hide()

        self._make_not_ready()
        self._make_thread(Models.RESNET50)
        self._connect_all()
        self._load_icons()

    def _load_icons(self):
        self.setWindowIcon(QIcon(":/icons/app.svg"))
        self.ui.actionOpen_Image.setIcon(QIcon(":/icons/open.svg"))
        self.ui.actionSettings.setIcon(QIcon(":/icons/settings.svg"))
        self.ui.actionExit.setIcon(QIcon(":/icons/exit.svg"))

    def _connect_all(self):
        self.ui.actionOpen_Image.triggered.connect(self.on_open_image)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.classify_btn.clicked.connect(self.push_work)
        self.ui.actionSettings.triggered.connect(self.on_open_settings)

    @Slot()
    def push_work(self):
        if self.img.isNull():
            return
        self.proc_dlg.show()
        mat = qimage_to_mat(self.img)
        self.worker.addTask(mat)
        res = self.worker.waitResult()
        self.ui.logger.append(f"<span style='color: red;'>{CLASSES[res]}</span>")
        self.proc_dlg.hide()

    @Slot()
    def on_open_settings(self):
        dlg = Settings(self.worker.model_type, self)
        dlg.accepted.connect(self.on_dlg_accept)
        dlg.open()

    @Slot()
    def on_dlg_accept(self):
        self._make_not_ready()
        dlg = self.sender()  # type: Settings
        model = dlg.get_model()
        self._make_thread(model)

    @Slot()
    def on_thread_ready(self):
        self._make_ready()

    def _make_thread(self, model):
        if self.worker is not None and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        self.worker = WorkerThread(model)
        self.worker.ready.connect(self.on_thread_ready)
        self.worker.start()

    def _make_not_ready(self):
        self.ui.classify_btn.setEnabled(False)
        self.ui.classify_btn.setToolTip(self.tr("Loading model, please wait"))

    def _make_ready(self):
        self.ui.classify_btn.setEnabled(True)
        self.ui.classify_btn.setToolTip("")

    @Slot()
    def on_open_image(self):
        fp, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Open Image"),
            QDir.homePath(),
            self.tr(IMAGE_FILTER)
        )
        if not fp:
            return
        self.img = QImage(fp)
        self.update_image()

    def update_image(self):
        self.ui.img_disp.set_image(self.img)

    def closeEvent(self, e):
        self.hide()
        self.worker.stop()
        self.worker.wait()
        super().closeEvent(e)
