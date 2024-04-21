from api.db_session import db_session
from api.db_session.Notes import Note
from api.api_resource.codes_error import *
from flask import jsonify


def create_note(content, private, id_user, session):
    note = Note(content=content, private=private, user_id=id_user)
    session.add(note)
    session.commit()
    _id = note.id
    session.close()
    return _id


def change_note(content, private, user_notes, note_id, session):
    _id = note_id
    for note in user_notes:
        if note.id == note_id:
            note.content = content
            note.private = private
            session.commit()
            session.close()
            return jsonify({"message": f"note {_id} change", "code": OK})
    session.close()
    return jsonify({"message": f"note {note_id} not found", "code": NOTFOUND})
