import sys

import qdarktheme
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import QtCore, QtWidgets

from interface.app_iterface import Ui_Form as MainForm
from interface.message_interface import Ui_Form as MessageForm

from api.Notes import Note
from api.Users import User
from api.api_com import login, delete, edit_note, get_note_by_id, create_note

from tests.test_data.data import *

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
	QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
	QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

user_global: None | User = None


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
		self.current_note_number = 0
		qdarktheme.setup_theme("light")
		self.set_connection()

	def set_connection(self):
		self.login_button.clicked.connect(self.login_click)
		self.send_button.clicked.connect(self.send_click)
		self.search_button.clicked.connect(self.read_click)
		self.main_tabs.currentChanged.connect(self.change_tab)
		self.next.clicked.connect(self.next_click)
		self.back.clicked.connect(self.back_click)
		self.edit_button.clicked.connect(self.edit_click)
		self.delete_button.clicked.connect(self.delete)

	def login_click(self):
		name = self.name_field.text()
		password = self.password_field.text()
		# отправка данных

		global user_global
		user = login({"username": name, "password": password})
		if isinstance(user, User):
			user_global = user
			self.username_label.setText(user_global.username)
			self.username_label_2.setText(user_global.username)
			self.username_label_3.setText(user_global.username)
			self.main_tabs.addTab(self.all_notes_tab, "")
			self.main_tabs.setCurrentIndex(3)
			self.main_tabs.removeTab(self.main_tabs.indexOf(self.login_tab))
			self.main_tabs.addTab(self.logout_tab, "")
			self.retranslateUi(self)
			dialog = Message("Login successful")
		else:
			dialog = Message(user["message"])
		dialog.show()
		dialog.exec_()
		self.name_field.setText("")
		self.password_field.setText("")

	def send_click(self):
		content = self.note_write_field.toPlainText()
		is_private = self.is_private.isChecked()
		res = create_note({"content": content, "private": is_private}, user_global)
		if isinstance(res, Note):
			dialog = Message("The note was created successfully, you can get it by ID, if private false: " + str(res.id))
			dialog.show()
			dialog.exec_()
			self.main_tabs.setCurrentIndex(1)
		else:
			dialog = Message(res["message"])
			dialog.show()
			dialog.exec_()

	def read_click(self, id=None):
		_id = self.search_id_field.text()
		res = get_note_by_id(_id)
		if isinstance(res, Note):
			self.note_read_field.setText(res.content)
			return
		mes = Message(res["message"])
		mes.show()
		mes.exec_()

	def change_tab(self):
		global user_global
		if self.main_tabs.currentWidget() == self.all_notes_tab:
			global user_global
			user_global = login({"username": user_global.username, "password": user_global.password})
			self.back.setVisible(True)
			self.next.setVisible(True)
			self.delete_button.setVisible(True)
			self.edit_button.setVisible(True)
			if len(user_global.notes) == 0:
				self.delete_button.setVisible(False)
				self.edit_button.setVisible(False)
				self.note_read_field_2.setText("")
			else:
				self.note_read_field_2.setText(user_global.notes[self.current_note_number].content)
			if self.current_note_number == 0:
				self.back.setVisible(False)
			if self.current_note_number >= len(user_global.notes) - 1:
				self.next.setVisible(False)
		elif self.main_tabs.currentWidget() == self.logout_tab:
			user_global = None
			self.main_tabs.removeTab(self.main_tabs.indexOf(self.all_notes_tab))
			self.main_tabs.addTab(self.login_tab, "")
			self.main_tabs.setCurrentIndex(2)
			self.main_tabs.removeTab(self.main_tabs.indexOf(self.logout_tab))
			self.retranslateUi(self)
			self.username_label.setText("")
			self.username_label_2.setText("")
			self.username_label_3.setText("")

	def next_click(self):
		self.current_note_number += 1
		self.change_tab()

	def back_click(self):
		self.current_note_number -= 1
		self.change_tab()

	def edit_click(self):
		content = user_global.notes[self.current_note_number].content
		private = user_global.notes[self.current_note_number].private
		self.main_tabs.setCurrentIndex(0)
		self.note_write_field.setText(content)
		self.is_private.setChecked(private)
		self.send_button.clicked.disconnect()
		self.send_button.clicked.connect(self.edit_send_click)

	def edit_send_click(self):
		user_global.notes[self.current_note_number].content = self.note_write_field.toPlainText()
		user_global.notes[self.current_note_number].private = self.is_private.isChecked()
		res = edit_note(user_global.notes[self.current_note_number], user_global)
		self.send_button.clicked.disconnect()
		self.send_button.clicked.connect(self.edit_click)
		self.main_tabs.setCurrentWidget(self.all_notes_tab)
		mes = Message(f"{res['message']}")
		mes.show()
		mes.exec_()

	def delete(self):
		delete(user_global, user_global.notes[self.current_note_number].id)
		del user_global.notes[self.current_note_number]
		self.current_note_number = 0
		self.change_tab()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.show()
	sys.exit(app.exec_())
