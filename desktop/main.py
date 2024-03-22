import sys

from desktop.interface_login import Ui_Form as login_form

from app import Ui_Form as main_form

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

username = None


class Login(QDialog, login_form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.login_but.clicked.connect(self.login_click)

	def login_click(self):
		name = self.name.text()
		password = self.password.text()
		# Отправка на api
		if True:  # логин успешен
			global username
			username = self.name.text()
			self.name.setText("you are in system")
			self.password.setText("you can close this window")

class App(QMainWindow, main_form):
	def __init__(self):
		self.username = "Anonymus"
		super().__init__()
		self.setupUi(self)
		self.login_tab.clicked.connect(self.login_tab_click)

	def login_tab_click(self):
		login = Login()
		login.show()
		login.exec_()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.show()
	sys.exit(app.exec_())
