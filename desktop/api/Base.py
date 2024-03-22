class Descripter:
    def __init__(self, js: dict):
        for key, value in js.items():
            if isinstance(value, str):
                exec(f"self.{key} = '{value}'")
            elif isinstance(value, list):
                local = {"_list": value, "self": self}
                exec(f"self.{key} = _list[:]", local)
            else:
                exec(f"self.{key} = {value}")
