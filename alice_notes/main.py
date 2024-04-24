from alice_yandex import *
from api import *

buttons = ButtonList()
buttons.add_button("написать", hide=True)
buttons.add_button("прочитать", hide=True)
buttons.add_button("заметки", hide=True)

alice = Alice(__name__)


@alice.on_start
def on_start(request: RequestData):
    alice.register_next_step(register_token, request.session["session_id"])
    return Response("Привет, введите свой токен")


def register_token(request: RequestData):
    token = request.request.original_utterance
    res = get_notes(token)
    if not isinstance(res, list):
        return Response(f"Сервер выдал ошибку: {res}, повторите попытку")
    res_str = "\n".join(
        [f"ID: {note.id}\nТекст:\n{note.content}\nПриватная:{note.private}\n----------------------------------\n" for
         note in res])
    print(res_str)
    return Response(res_str)


@alice.on_message
def on_message(request: RequestData):
    return Response(f"{request.request.original_utterance}")


alice.run(port="8888")
