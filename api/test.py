from requests import get, post, put, delete

print(get("http://127.0.0.1:5000/api/v2/notes/1").json())  # error not found


print(get("http://127.0.0.1:5000/api/v2/users/random_username").json())  # not found

print(post("http://127.0.0.1:5000/api/v2/users", json={"username": "test1", "password": "123456", "notes": [
	{"content": "test_note_1", "private": False}, {"content": "test_note_2", "private": True}
]}).json())  # create user

print(get("http://127.0.0.1:5000/api/v2/notes/1").json())  # get note
print(get("http://127.0.0.1:5000/api/v2/notes/2").json())  # not found because 2 is private

print(get("http://127.0.0.1:5000/api/v2/users/test1").json())  # not found


