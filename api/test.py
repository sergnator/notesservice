from requests import get, post, put, delete

# database empty
print(get("http://127.0.0.1:5000/api/v2/notes/1").json())  # error not found

print(get("http://127.0.0.1:5000/api/v2/users/random_username").json())  # not found

print(post("http://127.0.0.1:5000/api/v2/users", json={"username": "test1", "password": "123456", "notes": [
    {"content": "test_note_1", "private": False}, {"content": "test_note_2", "private": True}
]}).json())  # create user

print(
    post("http://127.0.0.1:5000/api/v2/users", json={"username": "test1", "password": "123"}).json())  # username taken

print(get("http://127.0.0.1:5000/api/v2/notes/1").json())  # get note
print(get("http://127.0.0.1:5000/api/v2/notes/2").json())  # not found because 2 private

print(get("http://127.0.0.1:5000/api/v2/users/test1").json())  # all user's notes not private
print(get('http://127.0.0.1:5000/api/v2/users',
          json={"username": "test1", "password": "123456"}).json())  # all user's notes

print(post('http://127.0.0.1:5000/api/v2/notes',
           json={'content': "something", "private": False, "username": "test1",
                 "password": "123456"}).json())  # create note
print(get("http://127.0.0.1:5000/api/v2/users/test1").json())  # all user's notes not private

print(get("http://127.0.0.1:5000/api/v2/notes/1").json())  # old note
print(put("http://127.0.0.1:5000/api/v2/notes/1",
          json={"username": "test1", "password": "123456", "content": "test_note_edit",
                "private": True}).json())  # edit note
print(get("http://127.0.0.1:5000/api/v2/notes/1").json())  # not found because private True
res = get('http://127.0.0.1:5000/api/v2/users', json={"username": "test1", "password": "123456"}).json()
for note in res["notes"]:
    if note["id"] == 1:
        print(note)  # edited note
        break
print(delete("http://127.0.0.1:5000/api/v2/notes/1", json={"username": "test1", "password": "123456"}).json())
print(get("http://127.0.0.1:5000/api/v2/notes/1").json())  # not found because note 1 deleted
print(get('http://127.0.0.1:5000/api/v2/users',
          json={"username": "test1", "password": "123456"}).json())  # all user's notes but note 1 deleted
