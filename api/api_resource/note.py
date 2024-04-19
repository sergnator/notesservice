from flask_restful import reqparse, Resource
from flask import jsonify

from .aborts import abort_if_note_not_found

from api.db_session import db_session
from api.db_session.Notes import Note
from api.db_session.Users import User

from .codes_error import *
from .token import check_token
from .functions.notes_functions import create_note, change_note

parser2 = reqparse.RequestParser()  # для парса аргументов юзера
parser2.add_argument("email", required=True)
parser2.add_argument("password", required=True)

parser = reqparse.RequestParser()  # для парса аргументов и юзера и заметок
parser.add_argument("email", required=True)
parser.add_argument("password", required=True)
parser.add_argument("content", required=True)
parser.add_argument("private", required=True, type=bool)

parser_auth_token = reqparse.RequestParser()
parser_auth_token.add_argument("auth-token", required=True)
parser_auth_token.add_argument("content", required=False)
parser.add_argument("private", required=False, type=bool)


class NoteResource(Resource):  # ресурс для заметки с параметрами
    def get(self, note_id):  # отправляет заметку если она не приватная по айди
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
        abort_if_note_not_found(note_id)
        session = db_session.create_session()
        args = parser.parse_args()
        user = session.query(User).filter(User.email == args["email"], User.password == args["password"]).first()
        if not user:
            session.close()
            return jsonify({"message": "email or password - wrong", "code": WRONG_PASSWORD_EMAIL})
        message = change_note(content=args["content"], private=args["private"], user_notes=user.notes, note_id=note_id,
                              session=session)
        return message


class NoteListResource(Resource):  # ресурс для заметок без параметров
    def get(self):  # отправляет все заметки которые не приватные
        session = db_session.create_session()
        notes = session.query(Note).filter(Note.private == 0).all()
        return jsonify({"notes": [item.to_dict() for item in notes], "code": OK})

    def post(self):  # создаёт заметку
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).filter(User.email == args["email"], User.password == args["password"]).first()
        if not user:
            session.close()
            return jsonify({"message": "email or password - wrong", "code": WRONG_PASSWORD_EMAIL})
        _id = create_note(args["content"], args["private"], user.id, session)
        return jsonify({"id": _id, "code": OK})


class AuthTokenNote(Resource):
    def post(self, id):
        session = db_session.create_session()

        args = parser.parse_args()
        if args["private"] or args["content"]:
            return jsonify({"message": "bad request", "code": BAD_REQUEST})

        id_ = check_token(args["auth-token"])
        if not id_:
            session.close()
            return jsonify({"message": "token expired", "code": TOKEN_EXPIRED})

        user = session.query(User).filter(id_ == User.id).first()
        note = Note(content=args['content'], private=args['private'], user_id=user.id)
        _id = create_note(note)
        return jsonify({"id": _id, "code": OK})

    def get(self):
        session = db_session.create_session()
        notes = session.query(Note).filter(Note.private == 0).all()
        session.close()
        return jsonify({"notes": [item.to_dict() for item in notes], "code": OK})


class NoteResourceToken(Resource):  # ресурс для заметки с параметрами
    def get(self, note_id):  # отправляет заметку если она не приватная по айди
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
        abort_if_note_not_found(note_id)
        session = db_session.create_session()
        args = parser2.parse_args()
        id_ = check_token(args["auth-token"])
        if not id_:
            session.close()
            return jsonify({"message": "token expired", "code": TOKEN_EXPIRED})
        user = session.query(User).filter(id_ == User.id).first()
        for note in user.notes:
            if note.id == note_id:
                session.delete(note)
                session.commit()
                return jsonify({"message": f"note {note_id} deleted", "code": OK})
        session.close()
        return jsonify({"message": "note not found", "code": NOTFOUND})

    def put(self, note_id):  # изменяет заметку
        abort_if_note_not_found(note_id)
        session = db_session.create_session()
        args = parser.parse_args()
        id_ = check_token(args["auth-token"])
        if not id_:
            session.close()
            return jsonify({"message": "token expired", "code": TOKEN_EXPIRED})
        user = session.query(User).filter(id_ == User.id).first()
        flag = False
        _id = change_note(content=args["content"], private=args["private"], user_notes=user.notes, note_id=note_id)
        if flag:
            return jsonify({"message": f"note {_id} change", "code": OK})
        session.close()
        return jsonify({"message": f"note {note_id} not found", "code": NOTFOUND})
