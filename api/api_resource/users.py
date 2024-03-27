from flask import jsonify
from flask_restful import reqparse, Resource

from api.db_session import db_session
from api.db_session.Notes import Note
from api.db_session.Users import User

from .aborts import abort_if_user_not_found
from .codes_error import *

parser = reqparse.RequestParser()  # для парса аргументов
parser.add_argument('username', required=True)
parser.add_argument('password', required=True)
parser.add_argument('notes', type=dict, action="append")


class UserResource(Resource):  # ресурс для юзера с параметрами
	def get(self, username):  # возвращает все не приватные заметки пользователя
		abort_if_user_not_found(username)
		session = db_session.create_session()
		user = session.query(User).filter(User.name == username).first()
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
		user = session.query(User).filter(User.name == args["username"]).first()
		if user:
			return jsonify({"message": "username id already used", "code": NAMETAKEN})
		if args["notes"] is None:
			args["notes"] = []
		user = User(name=args["username"], password=args["password"],
					notes=[Note(content=note['content'], private=note["private"]) for note in args["notes"]])
		session.add(user)
		session.commit()
		_id = user.id
		session.close()
		return jsonify({"id": _id, "code": OK})

	def get(self):
		db_session.global_init("db.db")
		args = parser.parse_args()
		if args["notes"] is not None:
			return jsonify({"message": "bad request", "code": BADREQUEST})
		session = db_session.create_session()
		user = session.query(User).filter(User.name == args["username"], User.password == args["password"]).first()
		if user:
			return {"notes": [note.to_dict() for note in user.notes], "code": OK, "user_id": user.id}
		session.close()
		return jsonify({"message": "username or password - wrong", "code": WRONG_PASSWORD_USERNAME})

