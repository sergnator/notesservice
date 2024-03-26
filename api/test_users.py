from requests import get, post, delete, put

print(post("http://127.0.0.1:5000/api/v2/notes", json={"content": 'new1', "private": False, "user_id": 1}).json())
print(put("http://127.0.0.1:5000/api/v2/notes/1",
          json={"username": "sergnator", "password": "123", "content": "new2", "private": True}).json())
