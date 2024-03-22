class Descripter:
	def __init__(self, js: dict):
		for key, value in js.items():
			exec(f"self.{key} = {value}")

