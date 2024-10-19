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

# Instantiate a dictionary for tasks
tasks_db = {}

# User has a username and a password
class User(BaseModel):
    username: str
    password: str

# Task object is a string
class Task(BaseModel):
    task: str

# Post to "login" API endpoint
@app.post("/login")
def login(user: User):
    # If the username exists AND the password is valid login
    if user.username in users and users[user.username] == user.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid username or password")

# Post to "tasks/{username} API endpoint"
@app.post("/tasks/{username}", response_model=List[str])
# Add a task to the task list
def add_task(username: str, task: Task):
    if username not in tasks_db:
        tasks_db[username] = []
    tasks_db[username].append(task.task)
    return tasks_db[username]

# Get from "tasks/{username} API endpoint"
@app.get("/tasks/{username}", response_model=List[str])
def get_tasks(username: str):
    return tasks_db.get(username, [])

