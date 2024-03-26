from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify

from .aborts import abort_if_note_not_found

from api.db_session import db_session
from api.db_session import db_session
from api.db_session.Notes import Note
from api.db_session.Users import User

from .codes_error import *

parser = reqparse.RequestParser()  # для парса аргументов
parser.add_argument('content', required=True)
parser.add_argument('private', required=True, type=bool)
parser.add_argument('user_id', required=True)

parser2 = reqparse.RequestParser()  # для парса аргументов юзера
parser2.add_argument("username", required=True)
parser2.add_argument("password", required=True)

parser3 = reqparse.RequestParser()  # для парса аргументов и юзера и заметок
parser3.add_argument("username", required=True)
parser3.add_argument("password", required=True)
parser3.add_argument("content", required=True)
parser3.add_argument("private", required=True, type=bool)


class NoteResource(Resource):  # ресурс для заметки с параметрами
	def get(self, note_id):  # отправляет заметку если она не приватная по айди
		db_session.global_init("db.db")
		abort_if_note_not_found(note_id)
		session = db_session.create_session()
		note = session.query(Note).filter(Note.private == False, Note.id == note_id).first()
		if note:
			return jsonify(note.to_dict())
		return jsonify({"message": f"note {note_id} not found", "code": NOTFOUND})

	def delete(self, note_id):
		db_session.global_init("db.db")
		abort_if_note_not_found(note_id)
		session = db_session.create_session()
		args = parser2.parse_args()
		user = session.query(User).filter(User.name == args["username"], User.password == args["password"]).first()
		if not user:
			return jsonify({"message": "username or password - wrong", "code": NOTFOUND})
		for note in user.notes:
			if note.id == note_id:
				session.delete(note)
				session.commit()
				return jsonify({"message": f"note {note_id} deleted", "code": NOTFOUND})
		return jsonify({"message": "note not found", "code": NOTFOUND})

	def put(self, note_id):
		db_session.global_init("db.db")
		abort_if_note_not_found(note_id)
		session = db_session.create_session()
		args = parser3.parse_args()
		user = session.query(User).filter(User.name == args["username"], User.password == args["password"]).first()
		if not user:
			return jsonify({"message": "username or password - wrong", "code": NOTFOUND})
		for note in user.notes:
			if note.id == note_id:
				note.content = args["content"]
				note.private = args["private"]
				session.commit()
				return jsonify({"message": f"note {note_id} change", "code": OK})
		return jsonify({"message": f"note {note_id} not found", "code": NOTFOUND})


class NoteListResource(Resource):  # ресурс для заметок без параметров
	def get(self):  # отправляет все заметки которые не приватные
		db_session.global_init("db.db")
		session = db_session.create_session()
		notes = session.query(Note).filter(Note.private == False).all()
		return jsonify([item.to_dict() for item in notes])

	def post(self):  # создаёт заметку
		db_session.global_init("db.db")
		args = parser.parse_args()
		session = db_session.create_session()
		note = Note(content=args['content'], private=args["private"], user_id=args["user_id"])
		session.add(note)
		session.commit()
		return jsonify({"id": note.id, "code": OK})
