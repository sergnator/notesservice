from alice_yandex import *
from api import *

buttons = ButtonList()
buttons.add_button("написать", hide=True)
buttons.add_button("прочитать", hide=True)
buttons.add_button("заметки", hide=True)

alice = Alice(__name__)

tokens = {}
notes = {}
notes_for_write = {}


@alice.on_start
def on_start(request: RequestData):  # если сессия новая
    alice.register_next_step(register_token, request.session["session_id"])
    return Response("Привет, введите свой токен")


def register_token(request: RequestData):  # получение токена
    token = request.request.original_utterance
    res = get_notes(token)
    if not isinstance(res, list):
        return Response(f"Сервер выдал ошибку: {res}, повторите попытку позже", end_session=True)
    tokens[request.session["session_id"]] = token
    return Response(f"Токен зарегистрирован", buttons=buttons)


@alice.on_message
def on_message(request: RequestData):
    return Response(f"не поняла вас")


@alice.message("заметки")
def notes_(request: RequestData):  # получение профиля пользователя
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


@alice.message("прочитать")
def read(request: RequestData):  # прочитать заметку
    alice.register_next_step(get_id, request.session["session_id"])
    return Response("Введите id заметки")


@alice.message("написать")
def write(request: RequestData):  # написать заметку
    alice.register_next_step(get_content, request.session["session_id"])
    return Response("Введите текст, который должен быть в заметке")


def get_content(request: RequestData):  # получения body заметки
    if request.request.original_utterance == " ":
        return Response("Заметка должна содержать хотя бы один символ")
    buttons_for_note = ButtonList()
    buttons_for_note.add_button("да", hide=True)
    buttons_for_note.add_button("нет", hide=True)
    notes_for_write[request.session["session_id"]] = request.request.original_utterance
    alice.register_next_step(get_private, request.session["session_id"])
    return Response("Сделать её приватной?", buttons=buttons_for_note)


def get_private(request: RequestData):  # получения приватности
    if request.request.original_utterance == "да":
        res = create_note({"content": notes_for_write[request.session["session_id"]], "private": True},
                          tokens[request.session["session_id"]])
        if isinstance(res, str):
            return Response(f"Сервер ответил с ошибкой: {res}", buttons=buttons)
        return Response(f"Заметка создана успешно.", buttons=buttons)
    elif request.request.original_utterance == "нет":
        res = create_note({"content": notes_for_write[request.session["session_id"]], "private": False},
                          tokens[request.session["session_id"]])
        if isinstance(res, str):
            return Response(f"Сервер ответил с ошибкой: {res}", buttons=buttons)
        return Response(f"Заметка создана успешно. Id: {res.id}", buttons=buttons)
    buttons_for_get_private = ButtonList()
    buttons_for_get_private.add_button("да")
    buttons_for_get_private.add_button("нет")
    alice.register_next_step(get_private, request)
    return Response("Немного не поняла вас. Сделать её приватной?", buttons=buttons_for_get_private)


def get_id(request: RequestData):  # получение id
    if not request.request.original_utterance.isdigit():
        return Response("id всегда число", buttons=buttons)
    res = read_note_by_id(request.request.original_utterance)
    if isinstance(res, str):
        return Response(f"Сервер ответил с ошибкой {res}", buttons=buttons)
    return Response(f"Id: {res.id}\n{res.content}\nприватность:{res.private}",
                    buttons=buttons)


def iter_notes(request: RequestData):  # итерироваться по всем запискам
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
