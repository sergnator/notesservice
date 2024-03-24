import sqlalchemy
from .db_session import SqlAlchemyBase


class Note(SqlAlchemyBase):
	__tablename__ = 'notes'

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	content = sqlalchemy.Column(sqlalchemy.String)
	username = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.name"))
