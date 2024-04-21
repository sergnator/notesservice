from requests import get, post, put, delete

print(19, post('http://127.0.0.1:5000/api/v2/token',
               # TODO: Запускаешь test.py получаешь токен в последнем токене и заменяешь
               json={'content': "something", "private": False,
                     "auth-token": "cuEWtynhYsksqewlKtmT"}).json())  # create note
