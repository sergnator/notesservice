import flask
from flask_restful import Api
from api_resource import note
from api_resource import users
from api.db_session import db_session

app = flask.Flask(__name__)
api = Api(app)

db_session.global_init("db.db")

api.add_resource(note.NoteResource, "/api/v2/notes/<int:note_id>")
api.add_resource(note.NoteListResource, "/api/v2/notes")
api.add_resource(users.UserResource, "/api/v2/users/<email_user>")
api.add_resource(users.UserNoParamResource, "/api/v2/users")
api.add_resource(users.UserNameResource, "/api/v2/username/<int:user_id>")
api.add_resource(note.NoteResourceToken, "/api/v2/token/<int:note_id>")

app.run()
