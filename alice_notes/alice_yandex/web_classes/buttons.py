import inspect


def name_var(x):
    caller_locals = inspect.currentframe().f_back.f_locals
    return [name for name, value in caller_locals.items() if x is value][-1]


class Button:
    def __init__(self, title: str, payload: dict = None, url: str = "", hide: bool = False):
        for type_, var in [(str, title), (str, url), (bool, hide)]:
            if not isinstance(var, type_):
                raise TypeError(f"Got {type(var)} of {name_var(var)} insted {type_}")
        self.title = title
        self.payload = None
        if payload is None:
            self.payload = dict()
        self.url = url
        self.hide = hide


class ButtonList:
    def __init__(self):
        self._list = []

    def add_button(self, title: str, payload: dict = None, url: str = "", hide: bool = False):
        self._list.append(Button(title, payload, url, hide))

    def remove_button(self, title: str):
        if not isinstance(title, str):
            raise TypeError(f"Got {type(title)} title insted str")
        for button in self._list:
            if button.title == title:
                del self._list[self._list.index(button)]
                return

    def change_button(self, title_old: str, title: str, payload: dict = None, url: str = "", hide: bool = False):
        self.remove_button(title_old)
        self.add_button(title, payload, url, hide)

    def all_titles(self):
        return [button.title for button in self._list]

    def __getitem__(self, item):
        return self._list[item]

    def __len__(self):
        return len(self._list)
