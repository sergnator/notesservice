from .Constans import *

from .Users import User
from .Notes import Note

import requests


def login(_user: dict):
	# принимает словарь типа {"username": "username", "password": "123456", notes(не обязательный): [Notes]"}
	res = requests.get(api_host + "users", json=_user).json()
	if res["code"] != OK:
		return res
	user_dict = dict()
	user_dict["notes"] = res["notes"]
	user_dict["username"] = _user["username"]
	user_dict["password"] = _user["password"]
	user_dict["id"] = res["user_id"]
	return User.from_dict(user_dict)


def get_note_by_id(id):  # TODO надо
	res = requests.get(api_host + "notes", params={"id": id})
	return res.json()


def post_note(note: dict, _user):
	res = requests.post(api_host + "notes", json=note).json()
	if res["code"] != OK:
		return res
	note["id"] = res["id"]
	_user.notes.append(Note.from_dict(note))
	return Note.from_dict(note)


def edit_note(note: Note, _user: User):
	res = requests.put(api_host + f"notes/{note.id}",
						json={"username": _user.username, "password": _user.password, "content": note.content,
						"private": note.private}).json()
	return res


def delete(_user: User, note_id):
	res = requests.delete(api_host + f"notes/{note_id}", json={"username": _user.username, "password": _user.password})
