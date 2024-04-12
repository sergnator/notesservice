from alice_yandex import *
from .api import *

buttons = ButtonList()
buttons.add_button("написать", hide=True)
buttons.add_button("прочитать", hide=True)
buttons.add_button("заметки", hide=True)

alice = Alice(__name__)

notes = {}

def send_note(request: RequestData):
    pass
@alice.on_start
def start(request: RequestData):
    return Response("Привет, выбери одну из кнопок", buttons=buttons)


@alice.message('написать')