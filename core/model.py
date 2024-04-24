import enum
import threading
from time import sleep

import torch
from queue import Queue, Empty
from torchvision.models import resnet50, ResNet50_Weights, resnet18, ResNet18_Weights, resnet34, ResNet34_Weights, \
    resnet101, ResNet101_Weights
from PySide6.QtCore import QEventLoop, QThread, QMutex, Signal
from PySide6.QtWidgets import QApplication
from torchvision.transforms import v2


def device():
    return 'cuda' if torch.cuda.is_available() else 'cpu'


class Models(enum.Enum):
    RESNET18 = 'resnet18'
    RESNET34 = 'resnet34'
    RESNET50 = 'resnet50'
    RESNET101 = 'resnet101'

    @classmethod
    def toList(cls):
        return [
            cls.RESNET18,
            cls.RESNET34,
            cls.RESNET50,
            cls.RESNET101
        ]

    def toModel(self):
        match self:
            case self.RESNET18:
                return resnet18(weights=ResNet18_Weights.DEFAULT).to(device())
            case self.RESNET34:
                return resnet34(weights=ResNet34_Weights.DEFAULT).to(device())
            case self.RESNET50:
                return resnet50(weights=ResNet50_Weights.DEFAULT).to(device())
            case self.RESNET101:
                return resnet101(weights=ResNet101_Weights.DEFAULT).to(device())


def build_model(model: Models = Models.RESNET50):
    model = model.toModel()
    model.eval()
    preprocess = v2.Compose([
        v2.RandomResizedCrop(size=(224, 224), antialias=True),  # Or Resize(antialias=True)
        v2.ToDtype(torch.float32, scale=True),  # Normalize expects float input
        v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return model, preprocess


class WorkerThread(QThread):
    ready = Signal()

    def __init__(self, model_t: Models = Models.RESNET50):
        super().__init__()
        self._t = model_t
        self.model = None
        self.preprocess = None
        self.tasks = Queue()
        self.results = Queue()
        self._lock = QMutex()
        self._stop = False

    @property
    def model_type(self):
        return self._t

    def stop(self):
        self._lock.lock()
        self._stop = True
        self._lock.unlock()

    def _is_stop(self):
        self._lock.lock()
        _stop = self._stop
        self._lock.unlock()
        return _stop

    def addTask(self, mat):
        self.tasks.put(mat)

    def allFinished(self):
        return self.tasks.all_tasks_done

    def waitResult(self):
        while True:
            try:
                res = self.results.get_nowait()
                break
            except Empty:
                QApplication.processEvents(
                    QEventLoop.ProcessEventsFlag.AllEvents,
                    100
                )
        return res

    def run(self):
        self.model, self.preprocess = build_model(self._t)
        # warm-up
        WARM_UP_SZ = (1, 3, 1000, 1000)
        mat = self.preprocess(torch.randn(WARM_UP_SZ)).to(device())
        _ = self.model(mat)
        self.ready.emit()
        while not self._is_stop():
            try:
                mat = self.tasks.get(block=False)
                mat = torch.tensor(mat).to(device()).permute((2, 0, 1)).unsqueeze(dim=0)
                mat = self.preprocess(mat)
                result = self.model(mat)
                result = torch.argmax(torch.squeeze(result)).to('cpu')
                self.results.put(result.item())
                self.tasks.task_done()
            except Empty:
                sleep(0.1)
