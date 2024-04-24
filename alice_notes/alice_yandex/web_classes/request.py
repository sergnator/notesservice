class RequestData:
	def __init__(self, request_data: dict):
		self.meta: dict = request_data['meta']
		self.session: dict = request_data['session']
		self.request: Request = Request(request_data['request'])
		self.version: str = request_data['version']


class Request:
	def __init__(self, request: dict):
		self.command: str = request["command"]
		self.original_utterance: str = request["original_utterance"]
		self.nlu: NLU = NLU(request['nlu'])
		self.markup: dict = request['markup']
		self.type: str = request['type']


class EnumNLU:
	Number = "YANDEX.NUMBER"
	FIO = "YANDEX.FIO"
	Date = "YANDEX.DATETIME"
	Geo = "YANDEX.GEO"


class NLU:
	def __init__(self, nlu: dict):
		self.tokens: list = nlu["tokens"]
		self.entities: list[Entity] = [Entity(entity) for entity in nlu["entities"]]
		self.intents: dict = nlu["intents"]


class Entity:
	def __init__(self, entity: dict):
		self.type: str = entity["type"]
		self.tokens: dict = entity['tokens']
		self.value: dict = entity["value"]
