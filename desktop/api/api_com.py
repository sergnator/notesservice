from Constans import *

from desktop.api.Users import User
from desktop.api.Notes import Note

import requests


def login(user: dict):
	res = requests.get(api_host + "users", json=user).json()
	if res["code"] != OK:
		return res
	user_dict = dict()
	user_dict["notes"] = [Note.from_dict(note) for note in res["notes"]]
	user_dict["username"] = user["username"]
	user_dict["password"] = user["password"]
	user_dict["id"] = res["user_id"]
	return User.from_dict(user_dict)


def get_note_by_id(id):
	res = requests.get(api_host + "notes", params={"id": id})
	return res.json()


def post_note(note: dict, _user):
	res = requests.post(api_host + "notes", json=note).json()
	if res["code"] != OK:
		return res
	note["id"] = res["id"]
	user.notes.append(Note.from_dict(note))
	return Note.from_dict(note)


def edit_note(note: Note):
	res = requests.put(api_host + "notes", json=note.to_dict())
	return res


print(requests.post("http://127.0.0.1:5000/api/v2/users",
                    json={"username": "1123", "password": "123"}).json())  # create user
user = login({"username": "1123", "password": "123"})
note1 = post_note({"user_id": user.id, "private": False, "content": "first"}, user)
print(user.notes[0].content)
