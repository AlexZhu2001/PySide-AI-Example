from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from ui.settings import Ui_Dialog
from core.model import Models


class Settings(QDialog):

    def __init__(self, model: Models, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        names = Models.toList()
        for i in range(4):
            self.ui.comboBox.setItemData(i, names[i], Qt.UserRole)
        self.ui.comboBox.setCurrentIndex(names.index(model))

    def get_model(self):
        return self.ui.comboBox.currentData(Qt.UserRole)
