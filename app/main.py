from fastapi import FastAPI, HTTPException, status
from .schemas import User

app = FastAPI()
users: list[User] = []

@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}

@app.get("/api/users")
def get_users():
    return users

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    for u in users:
        if u.user_id == user_id:
            return 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    if any(u.user_id == user.user_id for u in users):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id already exists")
    users.append(user)
    return user

@app.put("/api/user/{user_id}")
def update_user(user: User):
    if any(u.user_id == user.user_id for u in users):
        for i,e in enumerate(User):
    
    return user


@app.delete("/api/user/{user_id}")
def delete_user(user_id: int, user: User):
    for u in users:
        if u.user_id == user_id:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="user successfully removed")
        users.remove(u)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
