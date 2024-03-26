from requests import get, post, delete

print(delete("http://127.0.0.1:5000/api/v2/notes/1", json={"username": "sergnator", "password": "123"}).json())


