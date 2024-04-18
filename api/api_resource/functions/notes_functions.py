from api.db_session import db_session


def create_note(note):
    db_session.global_init("db.db")
    session = db_session.create_session()
    session.add(note)
    _id = note.id
    session.commit()
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

