from .Constans import *

from .Users import User
from .Notes import Note

import requests


def get_note_by_id(_id):
    # получаем заметку
    res = requests.get(api_host + f"notes/{_id}").json()
    if res["code"] == OK:
        return Note.from_dict({"content": res["content"], "private": False})
    return res["message"]  # сообщение об ошибке


def create_note(note: dict, _token: str):
    _dict = note.copy()
    _dict.update({"auth-token": _token})
    res = requests.post(api_host + "token", json=_dict).json()
    if res["code"] != OK:
        return res["message"]  # сообщение об ошибке
    note["id"] = res["id"]
    return Note.from_dict(note)


def read_note_by_id(_id):
    res = requests.get(api_host + f"notes/{_id}").json()
    if res["code"] != OK:
        return res["message"]
    return Note.from_dict(res)


def get_notes(_token: str):
    res = requests.get(api_host + "token", json={"auth-token": _token}).json()
    if res["code"] != OK:
        return res["message"]
    return [Note.from_dict(note) for note in res["notes"]]
