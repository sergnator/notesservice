import typing
import logging

from flask import Flask, request
from .web_classes import RequestData, to_json_from_class
from .images.image import ImageLoader


class Alice:
    def __init__(self, *args, debug=False, **kwargs):
        self.__message_handler = dict()
        self.__func_on_message = None
        self.__func_start = None
        self.__func_next_step = None
        self.redirect_all = False
        self.__redirected_func = None
        self.app = Flask(*args, **kwargs)
        self.__next_step_cache = {}
        if debug:
            logging.basicConfig(level=logging.DEBUG)

    def set_redirect_function(self, function: typing.Callable):
        self.__valid_function(function)
        self.__redirected_func = function

    def redirect(self, function: typing.Callable):
        self.set_redirect_function(function)
        return function

    def set_start_function(self, function: typing.Callable):
        self.__valid_function(function)
        self.__func_start = function

    def on_start(self, function: typing.Callable):
        self.set_start_function(function)
        return function

    def registrate_on_message(self, function: typing.Callable):
        self.__valid_function(function)
        self.__func_on_message = function

    def on_message(self, function: typing.Callable):
        self.registrate_on_message(function)
        return function

    def register_next_step(self, function: typing.Callable, _id):
        self.__valid_function(function)

        def wrapper(request_data: RequestData, alice: Alice):
            alice.__next_step_cache[request_data.session["session_id"]] = None
            return function(request_data)

        self.__next_step_cache[_id] = wrapper

    def registrate_message(self, function: typing.Callable, command_words: str | list[str]):
        self.__valid_function(function)
        self.__valid_command_words(command_words)
        self.__message_handler[function] = []
        if isinstance(command_words, str):
            self.__message_handler[function].append(command_words)
            return
        self.__message_handler[function] += command_words

    def message(self, command_words: str | list[str]):
        def wrapper(function):
            self.registrate_message(function, command_words)
            return function

        return wrapper

    def run(self, *args, clean: ImageLoader | None = None, **kwargs):
        self.app.add_url_rule("/post", None, self.__on_message, methods=["POST"])
        self.app.run(*args, **kwargs)
        if clean is not None and isinstance(clean, ImageLoader):
            clean.clear()
        elif not isinstance(clean, ImageLoader) and clean is not None:
            raise TypeError(f"Got {type(clean)} clean insted ImageLoader")

    def __on_message(self):
        request_data = RequestData(request.get_json())
        if request_data.session['new']:
            logging.debug("new session")
            return to_json_from_class(self.__func_start(request_data), request_data)

        if self.redirect_all:
            logging.debug("redirect_all function start")
            return to_json_from_class(self.__redirected_func(request_data), request_data)
        if self.__next_step_cache.get(request_data.session['session_id'], None) is not None:
            logging.debug("next step function")
            return to_json_from_class(self.__next_step_cache.get(request_data.session["session_id"])(request_data, self), request_data)
        for func, words in self.__message_handler.items():
            for word in words:
                if word in request_data.request.command.lower():
                    logging.debug(f"handler on word: {words}")
                    return to_json_from_class(func(request_data), request_data)
        logging.debug("handler on all message")
        return to_json_from_class(self.__func_on_message(request_data), request_data)

    def __valid_command_words(self, command_words):
        if not isinstance(command_words, str) and not isinstance(command_words, list):
            raise TypeError(f"Got {type(command_words)} command_words instead str or list of str")
        if isinstance(command_words, list):
            if len(command_words) == 0:
                raise TypeError(f"Command_words length must be greater than zero")
            if not all(map(lambda x: isinstance(x, str), command_words)):
                raise TypeError(f"command_words elements must be of type str")

    def __valid_function(self, function):
        if not isinstance(function, typing.Callable):
            raise TypeError(f"Got {type(function)} function insted Callable")
