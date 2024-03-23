import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import QtCore, QtWidgets

from app_iterface import Ui_Form as MainForm
from message_interface import Ui_Form as MessageForm

from api.Notes import Note
from api.Users import User

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
	QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
	QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

username = None


class Message(QDialog, MessageForm):
	def __init__(self, message):
		super().__init__()
		self.setupUi(self)
		self.message_label.setText(message)
		self.OK_button.clicked.connect(self.deleteLater)


class App(QMainWindow, MainForm):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.login_button.clicked.connect(self.login_click)
		self.send_button.clicked.connect(self.send_click)
		self.search_button.clicked.connect(self.read_click)

	def login_click(self):
		name = self.name_field.text()
		password = self.password_field.text()
		# отправка данных
		dialog = Message("Login failed")
		if name == '123' and password == '123':  # аналог проверки данных
			global username
			username = User.from_dict({"name": '123', "password": '123'})
			self.username_label.setText(username.username)
			self.username_label_2.setText(username.username)
			self.username_label_3.setText(username.username)
			dialog = Message("Login successful")
		dialog.show()
		dialog.exec_()
		self.name_field.setText("")
		self.password_field.setText("")

	def send_click(self):
		content = self.note_write_field.toPlainText()
		is_private = self.is_private.isChecked()
		res = {"result": True, "id": "11"}  # типа запрос
		dialog = Message("Error")
		if res["result"]:
			dialog = Message("The note was created successfully, you can get it by ID: " + res["id"])
		dialog.show()
		dialog.exec_()

	def read_click(self):
		id = self.search_id_field.text()
		res = {"content": "gasgashashah", "username": "124124",
		       "is_private": False}  # если is_private True то запрос не должен приходить, либо заменить можно content
		note = Note.from_dict(res)
		self.note_read_field.setText(note.content)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.show()
	sys.exit(app.exec_())
