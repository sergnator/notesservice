from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify

from api.db_session import db_session
from aborts import abort_if_note_not_found

parser = reqparse.RequestParser()
parser.add_argument('content', required=True)
parser.add_argument('is_private', required=True, type=bool)
parser.add_argument('username', required=True, type=int)


class NoteResource(Resource):
	def get(self, note_id):
		abort_if_note_not_found(note_id)
		session = db_session.create_session()
		note = session.query().get(note_id)
		return jsonify()