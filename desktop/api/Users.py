import json

from .Base import Descripter
from .Notes import Note


class User(Descripter):  # класс пользователя
    """на вход объект на подобии:
        {
        "username": "username",
        "password": "123456",
        "notes": [
            {"name": "name of note",
            "username": "username",
            "content": "all text of note",
            "private": false || true},
            {...}, ...]
        }"""
    username = None
    password = None
    notes: list[Note] = None
    id = None

    @staticmethod
    def from_dict(_dict: dict):  # получает словарь и возвращает экземпляр класса
        _dict = _dict.copy()
        if "notes" in _dict.keys():
            _dict["notes"] = [Note.from_dict(el) for el in
                              _dict["notes"]]  # первращение всех dict of note в экземпляр Note
        return User(_dict)

    @staticmethod
    def from_json(js: str):  # получает строку формата js и возвращает экземпляр класса
        return User.from_json(json.loads(js))

    def to_dict(self):
        return {"username": self.username, "password": self.password, "notes": [note.to_dict() for note in self.notes],
                "id": self.id}
