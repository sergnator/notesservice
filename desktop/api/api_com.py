from .Constans import *

from .Users import User
from .Notes import Note

import requests


def login(_user: dict):
    # принимает словарь типа
    # {"password": "123456", "email": "email@emal.com", notes(не обязательный): [Notes]"}
    res = requests.get(api_host + "users", json=_user).json()
    if res["code"] != OK:
        return res
    user_dict = dict()
    user_dict["notes"] = res["notes"]
    user_dict["username"] = res["username"]
    user_dict["password"] = _user["password"]
    user_dict["email"] = _user["email"]
    user_dict["id"] = res["user_id"]
    return User.from_dict(user_dict)


def get_note_by_id(_id):
    # получаем заметку
    res = requests.get(api_host + f"notes/{_id}").json()
    if res["code"] == OK:
        return Note.from_dict({"content": res["content"], "private": False})
    return res['message']


def create_note(note: dict, _user: User):
    _dict = note.copy()
    _dict.update({"username": _user.username, "password": _user.password, "email": _user.email})
    res = requests.post(api_host + "notes", json=_dict).json()
    if res["code"] != OK:
        return res['message']
    note["id"] = res["id"]
    _user.notes.append(Note.from_dict(note))
    return Note.from_dict(note)


def edit_note(note: Note, _user: User):
    res = requests.put(api_host + f"notes/{note.id}",
                       json={"username": _user.username, "password": _user.password, "content": note.content,
                             "private": note.private, "email": _user.email}).json()
    return res


def delete(_user: User, note_id):
    res = requests.delete(api_host + f"notes/{note_id}",
                          json={"username": _user.username, "password": _user.password, "email": _user.email})
