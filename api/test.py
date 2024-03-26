from requests import get, post

print(post("http://127.0.0.1:5000/api/v2/users", json={"username": "1", "password": "123", "notes": [
	{"content": "first not private", "private": False}, {"content": "second not private", "private": False},
	{"content": "third private", "private": True}]}).json())  # create user
print(get("http://127.0.0.1:5000/api/v2/users/1").json())  # get not private notes of user
print(get("http://127.0.0.1:5000/api/v2/users",
		json={"username": "1", "password": "123"}).json())  # get all notes of user
