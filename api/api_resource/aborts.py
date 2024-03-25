from api.db_session import db_session
from flask_restful import abort
from api.db_session.Notes import Note
from api.db_session.Users import User


def abort_if_note_not_found(note_id):
	db_session.global_init("db.db")
	session = db_session.create_session()
	news = session.query(Note).filter(Note.private == False, Note.id == note_id)
	if not news:
		abort(404, message=f"Note {note_id} not found")


def abort_if_user_not_found(username):
	db_session.global_init("db.db")
	session = db_session.create_session()
	user = session.query(User).filter(User.name == username).first()
	if not user:
		abort(404, message=f"User {username} not found")
