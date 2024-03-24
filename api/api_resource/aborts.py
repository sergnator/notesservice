from api.db_session import db_session
from flask_restful import abort


def abort_if_note_not_found(note_id):
	session = db_session.create_session()
	news = session.query().get(note_id)
	if not news:
		abort(404, message=f"Note: {note_id} not found")


def abort_if_user_not_found(user_id):
	session = db_session.create_session()
	news = session.query().get(user_id)
	if not news:
		abort(404, message=f"User: {user_id} not found")
