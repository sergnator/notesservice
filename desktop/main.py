import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel


class App(QApplication, QMainWindow):
    def __init__(self):
        super().__init__()

    def setup_ui(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())