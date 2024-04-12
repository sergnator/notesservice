from flask_restful import reqparse, Resource
from flask import jsonify

from .aborts import abort_if_note_not_found

from api.db_session import db_session
from api.db_session.Notes import Note
from api.db_session.Users import User

from .codes_error import *

parser2 = reqparse.RequestParser()  # для парса аргументов юзера
parser2.add_argument("email", required=True)
parser2.add_argument("password", required=True)

parser = reqparse.RequestParser()  # для парса аргументов и юзера и заметок
parser.add_argument("email", required=True)
parser.add_argument("password", required=True)
parser.add_argument("content", required=True)
parser.add_argument("private", required=True, type=bool)


class NoteResource(Resource):  # ресурс для заметки с параметрами
    def get(self, note_id):  # отправляет заметку если она не приватная по айди
        db_session.global_init("db.db")
        abort_if_note_not_found(note_id)
        session = db_session.create_session()
        note = session.query(Note).filter(Note.private == 0, Note.id == note_id).first()
        if note:
            _dict = note.to_dict()
            _dict.update({"code": OK})
            session.close()
            return jsonify(_dict)  # заметка успешно найдена и не приватна
        session.close()
        return jsonify(
            {"message": f"note {note_id} not found", "code": NOTFOUND})  # заметка или не найдена - или приватна

    def delete(self, note_id):  # удаляет заметку
        db_session.global_init("db.db")
        abort_if_note_not_found(note_id)
        session = db_session.create_session()
        args = parser2.parse_args()
        user = session.query(User).filter(User.email == args["email"], User.password == args["password"]).first()
        if not user:
            session.close()
            return jsonify({"message": "email or password - wrong", "code": WRONG_PASSWORD_EMAIL})
        for note in user.notes:
            if note.id == note_id:
                session.delete(note)
                session.commit()
                return jsonify({"message": f"note {note_id} deleted", "code": OK})
        session.close()
        return jsonify({"message": "note not found", "code": NOTFOUND})

    def put(self, note_id):  # изменяет заметку
        db_session.global_init("db.db")
        abort_if_note_not_found(note_id)
        session = db_session.create_session()
        args = parser.parse_args()
        user = session.query(User).filter(User.email == args["email"], User.password == args["password"]).first()
        if not user:
            session.close()
            return jsonify({"message": "email or password - wrong", "code": WRONG_PASSWORD_EMAIL})
        for note in user.notes:
            if note.id == note_id:
                note.content = args["content"]
                note.private = args["private"]
                session.commit()
                session.close()
                return jsonify({"message": f"note {note_id} change", "code": OK})
        session.close()
        return jsonify({"message": f"note {note_id} not found", "code": NOTFOUND})


class NoteListResource(Resource):  # ресурс для заметок без параметров
    def get(self):  # отправляет все заметки которые не приватные
        db_session.global_init("db.db")
        session = db_session.create_session()
        notes = session.query(Note).filter(Note.private == 0).all()
        session.close()
        return jsonify({"notes": [item.to_dict() for item in notes], "code": OK})

    def post(self):  # создаёт заметку
        db_session.global_init("db.db")
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).filter(User.email == args["email"], User.password == args["password"]).first()
        if not user:
            session.close()
            return jsonify({"message": "email or password - wrong", "code": WRONG_PASSWORD_EMAIL})
        note = Note(content=args['content'], private=args["private"], user_id=user.id)
        session.add(note)
        session.commit()
        _id = note.id
        session.close()
        return jsonify({"id": _id, "code": OK})
