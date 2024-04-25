from requests import get, post, put, delete

print(3, post("http://127.0.0.1:5000/api/v2/users",
              json={"email": "email23@email.com", "username": "test23", "password": "123456"}).json())  # create user

user = get('http://127.0.0.1:5000/api/v2/users',
           json={"username": "test23", "password": "123456",
                 "email": "email23@email.com"}).json()
print(user["auth-token"])

print(post("http://127.0.0.1:5000/api/v2/token",
           json={"content": "test with token", "private": False, "auth-token": user["auth-token"]}).json())
print(get("http://127.0.0.1:5000/api/v2/notes/1").json())

print(put("http://127.0.0.1:5000/api/v2/token",
          json={"content": "test with token edit", "private": False, "id": 1, "auth-token": user["auth-token"]}).json())
print(get("http://127.0.0.1:5000/api/v2/notes/1").json())
print(delete("http://127.0.0.1:5000/api/v2/token",
          json={"id": 1, "auth-token": user["auth-token"]}).json())
print(get("http://127.0.0.1:5000/api/v2/notes/1").json())