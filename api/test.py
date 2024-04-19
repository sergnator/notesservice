import sys

from requests import get, post, put, delete

# database empty
print(1, get("http://127.0.0.1:5000/api/v2/notes/1").json())  # error not found

print(2, get("http://127.0.0.1:5000/api/v2/users/random_username@email.com").json())  # not found

print(3, post("http://127.0.0.1:5000/api/v2/users",
           json={"email": "email23@email.com", "username": "test23", "password": "123456", "notes": [
               {"content": "test_note_1", "private": False}, {"content": "test_note_2", "private": True}
           ]}).json())  # create user

print(4,
    post("http://127.0.0.1:5000/api/v2/users",
         json={"email": "email23@email.com", "username": "test23", "password": "123456"}).json())  # email taken

print(5, get("http://127.0.0.1:5000/api/v2/notes/1").json())  # get note
print(6, get("http://127.0.0.1:5000/api/v2/notes/2").json())  # not found because 2 private

print(7, get("http://127.0.0.1:5000/api/v2/users/email23@email.com").json())  # all user's notes not private
print(8, get('http://127.0.0.1:5000/api/v2/users',
          json={"username": "test23", "password": "123456", "email": "email23@email.com"}).json())  # all user's notes

print(9, post('http://127.0.0.1:5000/api/v2/notes',
           json={'content': "something", "private": False, "username": "test23",
                 "password": "123456", "email": "email23@email.com"}).json())  # create note
print(10, get("http://127.0.0.1:5000/api/v2/users/email23@email.com").json())  # all user's notes not private

print(11, get("http://127.0.0.1:5000/api/v2/notes/1").json())  # old note
print(12, put("http://127.0.0.1:5000/api/v2/notes/1",
          json={"username": "test23", "password": "123456", "content": "test_note_edit", "email": "email23@email.com",
                "private": True}).json())  # edit note
print(13, get("http://127.0.0.1:5000/api/v2/notes/1").json())  # not found because private True

res = get('http://127.0.0.1:5000/api/v2/users',
          json={"username": "test23", "password": "123456", "email": "email23@email.com"}).json()
for note in res["notes"]:
    if note["id"] == 1:
        print(note)  # edited note
        break

print(14, delete("http://127.0.0.1:5000/api/v2/notes/1",
             json={"username": "test1", "password": "12345", "email": "email23@email.com"}).json())  # wrong data user

print(15, delete("http://127.0.0.1:5000/api/v2/notes/1",
             json={"username": "test23", "password": "123456", "email": "email23@email.com"}).json())
print(16, get("http://127.0.0.1:5000/api/v2/notes/1").json())  # not found because note 1 deleted
print(17, get('http://127.0.0.1:5000/api/v2/users',
          json={"username": "test23", "password": "123456",
                "email": "email23@email.com"}).json())  # all user's notes but note 1 deleted

print(18, get('http://127.0.0.1:5000/api/v2/'))
