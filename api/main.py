import flask
from flask_restful import Api
from api_resource import note
from db_session import Notes
from db_session import db_session

app = flask.Flask(__name__)
api = Api(app)
api.add_resource(note.NoteResource, "/api/v2/notes/<int:note_id>")
db_session.global_init("db.db")
note = Notes.Note(content="1245")
session = db_session.create_session()
session.add(note)
session.commit()

app.run()
