import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Note(SqlAlchemyBase, SerializerMixin):
	__tablename__ = 'notes'

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	content = sqlalchemy.Column(sqlalchemy.String)
	username = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.name"))
	private = sqlalchemy.Column(sqlalchemy.Boolean)
