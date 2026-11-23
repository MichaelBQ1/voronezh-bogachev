from PyQt6.QtWidgets import QPushButton


class Ui_MainWindow:
    def setupUi(self, window):
        window.setFixedSize(600, 450)
        window.setWindowTitle("Цветные окружности")
        self.pushButton = QPushButton("Добавить окружность", window)
        self.pushButton.setGeometry(200, 15, 200, 35)
