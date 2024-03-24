from .Base import Descripter

import json


class Note(Descripter):
	"""на вход объект на подобии:
		{
		"username": "name of user",
		"content": "all text of note",
		"private": false || true
		}"""
	username = None
	content = None
	private = False

	@staticmethod
	def from_dict(_dict):  # получает словарь и возвращает экземпляр класса
		return Note(_dict)

	@staticmethod
	def from_json(js: str):  # получает строку формата js и возвращает экземпляр класса
		return Note.from_json(json.loads(js))
