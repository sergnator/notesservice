from requests import get, post

print(post("http://127.0.0.1:5000/api/v2/users", json={"username": "1", "password": "123"}).json())  # create user
print(post("http://127.0.0.1:5000/api/v2/users",
           json={"username": "1", "password": "123"}).json())  # error name is already taken

