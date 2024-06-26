import datetime
import random
import string


def check_token(auth_token):  # проверка на подлинность токена
    now = datetime.datetime.now()
    for key, value in cache.items():
        if value[1] == auth_token:
            if (value[0] - now).days >= 1:
                cache[key] = (now, generate_auth_token(DEFAULT_COUNT))
                return False
            else:
                return key
    return False


def generate_auth_token(count):  # генерирует токен
    token = ''.join(random.choices(string.ascii_letters, k=count))
    while token in [value[0] for value in cache.values()]:
        token = ''.join(random.choices(string.ascii_letters, k=count))
    return token


def get_token(_id):  # получает токен
    if not check_token(cache.get(_id, [1, 2])[1]):
        cache[_id] = (datetime.datetime.now(), generate_auth_token(DEFAULT_COUNT))
        return cache[_id][1]
    return cache[_id][1]


cache = {}
DEFAULT_COUNT = 20
