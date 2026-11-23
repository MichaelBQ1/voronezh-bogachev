import sys
from random import randint

from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QApplication, QMainWindow

from ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.circles = []
        self.pushButton.clicked.connect(self.add_circle)

    def add_circle(self):
        diameter = randint(20, 150)
        x = randint(10, self.width() - diameter - 10)
        y = randint(70, self.height() - diameter - 10)
        color = QColor(randint(0, 255), randint(0, 255), randint(0, 255))
        self.circles.append((x, y, diameter, color))
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        for x, y, diameter, color in self.circles:
            painter.setPen(QPen(color, 3))
            painter.drawEllipse(x, y, diameter, diameter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
