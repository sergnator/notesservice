import sys
from desktop.inretface import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow


class App(QMainWindow, Ui_Form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setup_ui()

	def setup_ui(self):
		self.username = "Anonymus"

	def login(self):
		name = self.name.text()
		password = self.password.text()
		# далее отправка на api и получения результатов
		# если ответ нормальный то мы меняем имя и теперь все отправки будут от этого имени
		self.username = name


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.show()
	sys.exit(app.exec_())
