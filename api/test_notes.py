from requests import get, post

print(get("http://127.0.0.1:5000/api/v2/notes/1").json())  # get note with id=1
print(get("http://127.0.0.1:5000/api/v2/notes").json())  # get all notes
print(post("http://127.0.0.1:5000/api/v2/notes", json={}).json())  # bad req
print(post("http://127.0.0.1:5000/api/v2/notes",
           json={"content": "гоша лох", "private": False, "user_id": "123"}).json())  # create note
print(get("http://127.0.0.1:5000/api/v2/notes/2").json())  # get created note
