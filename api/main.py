import flask
from flask_restful import Api
from api_resource import note
from api_resource import users

app = flask.Flask(__name__)
api = Api(app)

api.add_resource(note.NoteResource, "/api/v2/notes/<int:note_id>")
api.add_resource(note.NoteListResource, "/api/v2/notes")
api.add_resource(users.UserResource, "/api/v2/users/<username>")
api.add_resource(users.UserNoParamResource, "/api/v2/users")



app.run()
