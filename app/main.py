from fastapi import FastAPI, HTTPException, status
from .schemas import User

app = FastAPI()
users: list[User] = []

@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}

# return key/value pair for an 'ok' status
@app.get("/health")
def health():
    return {"status": "ok"}

# return all users
@app.get("/api/users")
def get_users():
    return users

# return user by user_id
@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    for u in users:
        if u.user_id == user_id:
            return 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

# create user, check if user_id exists or if student_id exists, 201_CREATED status if successful
@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    if any(u.user_id == user.user_id for u in users):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id already exists")
    if any(u.student_id == user.student_id for u in users):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="student_id already exists")
    users.append(user)
    return user

# update user info
@app.put("/api/users/{user_id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id: int, user: User):
    for i,e in enumerate(users):  # e = members of 'users' list/User object & i = index of the object
        if e.user_id == user_id:
            users[i] = user
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

# delete user by user_id
@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    for i,e in enumerate(users):
        if e.user_id == user_id:
            users.pop(i)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")