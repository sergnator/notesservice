from requests import get, post


print(get("http://127.0.0.1:5000/api/v2/notes/1").json())
print(get("http://127.0.0.1:5000/api/v2/notes").json())
print(post("http://127.0.0.1:5000/api/v2/notes", json={}).json())
print(post("http://127.0.0.1:5000/api/v2/notes", json={"content": "гоша лох", "private": False, "username": "123"}).json())
print(get("http://127.0.0.1:5000/api/v2/notes/2").json())

