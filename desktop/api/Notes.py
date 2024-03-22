from Base import Descripter


class Note(Descripter):
	name = None
	username = None
	content = None
	private = False

	@staticmethod
	def from_json(js: dict):
		return Note(js)
