class Descripter:
    def __init__(self, js: dict):
        for key, value in js.items():
            local = {"value": value, "self": self}
            exec(f"self.{key} = value", local)
