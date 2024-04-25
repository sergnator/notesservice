import logging
import typing

from alice_yandex.web_classes.request import RequestData, EnumNLU
from alice_yandex.Alice import Alice
from alice_yandex.web_classes import Response


class UserStorage:
    def __init__(self, alice):
        if not isinstance(alice, Alice):
            raise TypeError(f"got {type(alice)} alice insted class Alice")
        self.__data = dict()
        self.alice = alice

    def __get_username(self, request: RequestData):
        logging.debug('start get_username')
        for entity in request.request.nlu.entities:
            if entity.type == EnumNLU.FIO:
                first_name = entity.value.get("first_name", None)
                if first_name is None:
                    logging.debug("abort get_username: invalid keywoard")
                    return Response("что-то не раслышала")
                else:
                    self.alice.redirect_all = False
                    self.__data[request.session['user']['user_id']] = first_name
                    logging.debug("get_username sucsses")
                    return Response(f"Приятно познакомится, {first_name}. " + self.message_plus)
        logging.debug("abort get_username: invalid keywoard")
        return Response("что-то не раслышала")

    def registrate_user(self, request: RequestData, message_plus=""):
        if not isinstance(message_plus, str):
            raise TypeError(f"Got {type(message_plus)} message_plus insted str")

        self.alice.redirect_all = True
        self.message_plus = message_plus
        self.alice.set_redirect_function(self.__get_username)

    def check_user(self, request: RequestData):
        return self.__data.get(request.session['user']['user_id'])
