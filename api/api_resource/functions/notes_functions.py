from api.db_session import db_session


def create_note(note):
    db_session.global_init("db.db")
    session = db_session.create_session()
    session.add(note)
    _id = note.id
    session.commit()
    session.close()
    return _id
