from .Base import Descripter

import json


class Note(Descripter):
	"""на вход объект на подобии:
		{
		"user_id": id,
		"content": "all text of note",
		"private": false || true
		}"""
	user_id = None
	content = None
	private = False
	id = None

	@staticmethod
	def from_dict(_dict):  # получает словарь и возвращает экземпляр класса
		return Note(_dict)

	@staticmethod
	def from_json(js: str):  # получает строку формата js и возвращает экземпляр класса
		return Note.from_json(json.loads(js))

	def to_dict(self):
		return {"username": self.user_id, "content": self.content, "private": self.private, "id": self.id}