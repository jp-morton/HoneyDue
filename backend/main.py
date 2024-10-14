from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

# Dummy user data for authentication
users = {
    "user1": "password1",
    "user2": "password2"
}

tasks_db = {}

class User(BaseModel):
    username: str
    password: str

class Task(BaseModel):
    task: str

@app.post("/login")
def login(user: User):
    if user.username in users and users[user.username] == user.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid username or password")

@app.post("/tasks/{username}", response_model=List[str])
def add_task(username: str, task: Task):
    if username not in tasks_db:
        tasks_db[username] = []
    tasks_db[username].append(task.task)
    return tasks_db[username]

@app.get("/tasks/{username}", response_model=List[str])
def get_tasks(username: str):
    return tasks_db.get(username, [])

# if __name__ == "main":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
