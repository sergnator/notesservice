from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify

from api.db_session import db_session
from .aborts import abort_if_note_not_found
from api.db_session import db_session

from api.db_session.Notes import Note

parser = reqparse.RequestParser()
parser.add_argument('content', required=True)
parser.add_argument('private', required=True, type=bool)
parser.add_argument('user_id', required=True)


class NoteResource(Resource):
	def get(self, note_id):
		db_session.global_init("db.db")
		abort_if_note_not_found(note_id)
		session = db_session.create_session()
		note = session.query(Note).filter(Note.private == False, Note.id == note_id).first()
		return jsonify(note.to_dict())


class NoteListResource(Resource):
	def get(self):
		db_session.global_init("db.db")
		session = db_session.create_session()
		notes = session.query(Note).filter(Note.private == False).all()
		return jsonify([item.to_dict() for item in notes])

	def post(self):
		db_session.global_init("db.db")
		args = parser.parse_args()
		session = db_session.create_session()
		note = Note(content=args['content'], private=args["private"], user_id=args["user_id"])
		session.add(note)
		session.commit()
		return jsonify({"id": note.id})
