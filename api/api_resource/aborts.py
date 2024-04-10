from flask_restful import abort

from api.db_session import db_session
from api.db_session.Notes import Note
from api.db_session.Users import User

from .codes_error import *


def abort_if_note_not_found(note_id):  # если заметка не найдена
    db_session.global_init("db.db")
    session = db_session.create_session()
    note = session.query(Note).filter(Note.id == note_id).first()
    if not note:
        abort(404, message=f"Note {note_id} not found", code=NOTFOUND)


def abort_if_user_not_found(user_email):  # если пользователь не найден
    db_session.global_init("db.db")
    session = db_session.create_session()
    user = session.query(User).filter(User.email == user_email).first()
    if not user:
        abort(404, message=f"User {user_email} not found", code=NOTFOUND)
