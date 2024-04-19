from api.db_session import db_session
from api.db_session.Notes import Note


def create_note(content, private, id_user):
    db_session.global_init("db.db")
    session = db_session.create_session()
    note = Note(content=content, private=private, user_id=id_user)
    session.add(note)
    session.commit()
    _id = note.id
    session.close()
    return _id


def change_note(content, private, user_notes, note_id):
    db_session.global_init("db.db")
    session = db_session.create_session()
    _id = note_id
    for note in user_notes:
        if note.id == note_id:
            note.content = content
            note.private = private
            session.commit()
            session.close()
            flag = True
            return _id, flag

