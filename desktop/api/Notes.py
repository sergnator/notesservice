from Base import Descripter

import json


class Note(Descripter):
	"""на вход объект на подобии:
		{"name": "name of note",
		"username": "name of user",
		"content": "all text of note",
		"private": false || true
		}"""
	name = None
	username = None
	content = None
	private = False

	@staticmethod
	def from_dict(_dict) -> Descripter:  # получает словарь и возвращает экземпляр класса
		return Note(_dict)

	@staticmethod
	def from_json(js: str) -> Descripter:  # получает строку формата js и возвращает экземпляр класса
		return Note.from_json(json.loads(js))
