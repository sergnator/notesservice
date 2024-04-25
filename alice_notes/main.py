from alice_yandex import *
from api import *
import ngrok

buttons = ButtonList()
buttons.add_button("написать", hide=True)
buttons.add_button("прочитать", hide=True)
buttons.add_button("заметки", hide=True)

alice = Alice(__name__)

tokens = {}
notes = {}


@alice.on_start
def on_start(request: RequestData):
    alice.register_next_step(register_token, request.session["session_id"])
    return Response("Привет, введите свой токен")


def register_token(request: RequestData):
    token = request.request.original_utterance
    res = get_notes(token)
    if not isinstance(res, list):
        return Response(f"Сервер выдал ошибку: {res}, повторите попытку позже", end_session=True)
    tokens[request.session["session_id"]] = token
    return Response(f"Токен зарегистрирован", buttons=buttons)


@alice.on_message
def on_message(request: RequestData):
    return Response(f"{request.request.original_utterance}")


@alice.message("заметки")
def notes_(request: RequestData):
    if request.session["session_id"] not in tokens.keys():
        return Response("Вам нужен токен", end_session=True)
    token = tokens.get(request.session["session_id"])
    res: list[Note] = get_notes(token)
    if not isinstance(res, list):
        return Response(f"Сервер выдал ошибку: {res}, повторите попытку позже", end_session=True)
    if len(res) == 0:
        return Response("У вас пока что нет заметок", buttons=buttons)
    current_note = 0
    notes[request.session["session_id"]] = (res, current_note)
    buttons_for_note = ButtonList()
    buttons_for_note.add_button("отмена")
    if len(res) > 1:
        buttons_for_note.add_button(">>")
    alice.register_next_step(iter_notes, request.session["session_id"])
    return Response(f"Id: {res[current_note].id}\n{res[current_note].content}\nприватность:{res[current_note].private}",
                    buttons=buttons_for_note)


def iter_notes(request: RequestData):
    notes_, current_note = notes[request.session["session_id"]]
    if request.request.original_utterance == ">>":
        if len(notes_) < 1:
            buttons_for_note = ButtonList()
            buttons_for_note.add_button("отмена")
            if 0 != current_note:
                buttons_for_note.add_button("<<")
            alice.register_next_step(iter_notes, request.session["session_id"])
            return Response("У вас нет больше записок", buttons=buttons_for_note)
        current_note += 1

    if request.request.original_utterance == "<<":
        if current_note == 0:
            buttons_for_note = ButtonList()
            buttons_for_note.add_button("отмена")
            if current_note == len(notes) - 1:
                buttons_for_note.add_button(">>")
            return Response("Это первая заметка")
        current_note -= 1

    if request.request.original_utterance == "отмена":
        del notes[request.session["session_id"]]
        return Response("отменяю", buttons=buttons)

    buttons_for_note = ButtonList()
    buttons_for_note.add_button("отмена")
    if current_note != 0:
        buttons_for_note.add_button("<<")
    if current_note != len(notes) - 1:
        buttons_for_note.add_button(">>")
    alice.register_next_step(iter_notes, request.session['session_id'])
    notes[request.session["session_id"]] = (notes_, current_note)
    return Response(
        f"Id: {notes_[current_note].id}\n{notes_[current_note].content}\nприватность:{notes_[current_note].private}",
        buttons=buttons_for_note)


alice.run(port="1000")
