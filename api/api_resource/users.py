from flask import jsonify
from flask_restful import reqparse, Resource

import random
import string
import datetime

from api.db_session import db_session
from api.db_session.Notes import Note
from api.db_session.Users import User

from .aborts import abort_if_user_not_found
from .codes_error import *
from .token import generate_auth_token, DEFAULT_COUNT, get_token, cache

parser = reqparse.RequestParser()  # для парса аргументов
parser.add_argument('username', required=False)
parser.add_argument('password', required=True)
parser.add_argument('notes', type=dict, action="append")
parser.add_argument("email", required=True)


class UserResource(Resource):  # ресурс для юзера с параметрами
    def get(self, email_user):  # возвращает все не приватные заметки пользователя
        abort_if_user_not_found(email_user)
        session = db_session.create_session()
        user = session.query(User).filter(User.email == email_user).first()
        notes = []
        for note in user.notes:
            if not note.private:
                notes.append(note)
        session.close()
        return jsonify({"notes": [note.to_dict() for note in notes], "code": OK})


class UserNoParamResource(Resource):
    def post(self):  # создаёт пользователя
        db_session.global_init("db.db")
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).filter(User.email == args["email"]).first()
        if user:
            session.close()
            return jsonify({"message": "email is already used", "code": NAME_TAKEN})

        if args["notes"] is None:
            args["notes"] = []

        user = User(name=args["username"], password=args["password"],
                    notes=[Note(content=note['content'], private=note["private"]) for note in args["notes"]],
                    email=args["email"])
        session.add(user)
        session.commit()
        _id = user.id
        session.close()

        token = cache[_id] = (datetime.datetime.now(), generate_auth_token(DEFAULT_COUNT))

        return jsonify({"id": _id, "code": OK, "message": "user created", "auth-token": token[1]})

    def get(self):  # возвращает всю информацию о пользователе
        db_session.global_init("db.db")
        args = parser.parse_args()
        if args["notes"] is not None:
            return jsonify({"message": "bad request", "code": BAD_REQUEST})

        session = db_session.create_session()
        user = session.query(User).filter(User.email == args["email"], User.password == args["password"]).first()
        if user is None:
            session.close()
            return jsonify({"message": "email or password - wrong", "code": WRONG_PASSWORD_EMAIL})

        res = {"notes": [note.to_dict() for note in user.notes], "code": OK, "user_id": user.id,
               "username": user.name, "auth-token": get_token(user.id)}
        session.close()
        return res


class UserNameResource(Resource):
    def get(self, user_id):  # возвращает имя пользователя
        db_session.global_init("db.db")
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            session.close()
            return jsonify({"message": "user not found", "code": NOTFOUND})
        username = user.name
        email = user.email
        session.close()
        return jsonify({"username": username, "email": email, "code": OK, "id": user_id})
