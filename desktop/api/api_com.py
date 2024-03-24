from Constans import *

from desktop.api.Users import User
from desktop.api.Notes import Note

import requests


def login(user: User):
	res = requests.get(api_host + "users", json=user.to_dict())
	return res.json()


def get_note_by_id(id):
	res = requests.get(api_host + "notes", params={"id": id})
	return res.json()


def post_note(note: Note):
	res = requests.post(api_host + "notes", json=note.to_dict())
	return res


def edit_note(note: Note):
	res = requests.put(api_host + "notes", json=note.to_dict())
	return res