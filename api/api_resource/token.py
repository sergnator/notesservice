import datetime
import random
import string


def check_token(auth_token):
    now = datetime.datetime.now()
    for key, value in cache.items():
        if value[1] == auth_token:
            if (value[0] - now).days >= 1:
                cache[key] = (now, generate_auth_token(DEFAULT_COUNT))
                return False
            else:
                return key
    return False


def generate_auth_token(count):
    token = ''.join(random.choices(string.ascii_letters, k=count))
    while token in [value[0] for value in cache.values()]:
        token = ''.join(random.choices(string.ascii_letters, k=count))
    return token


cache = {}
DEFAULT_COUNT = 20