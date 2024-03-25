from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify

from api.db_session import db_session
from .aborts import abort_if_user_not_found
from api.db_session import db_session

from api.db_session.Users import User
from api.db_session.Notes import Note

parser = reqparse.RequestParser()
parser.add_argument('username', required=True)
parser.add_argument('password', required=True)
parser.add_argument('notes')


class UserResource(Resource):
	def get(self, username):
		abort_if_user_not_found(username)
		session = db_session.create_session()
		user = session.query(User).filter(User.name == username).first()
		notes = []
		for note in user.notes:
			if not note.private:
				notes.append(note)
		return jsonify({"notes": [note.to_dict() for note in notes]})


class UserListResource(Resource):
	def post(self):
		db_session.global_init("db.db")
		args = parser.parse_args()
		user = User(name=args["username"], password=args["password"])
		session = db_session.create_session()
		session.add(user)
		session.commit()
		return jsonify({"id": user.id})