from Base import Descripter


class User(Descripter):
	username = None
	password = None
	notes = None
	@staticmethod
	def from_json(js):
		return User(js)