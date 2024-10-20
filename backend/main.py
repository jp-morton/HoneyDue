from fastapi import FastAPI, HTTPException, Request

from pydantic import BaseModel
from typing import List
import uvicorn
import h5py
import numpy as np

from libraries.user import User
from libraries.task import Task
from temp_database.data_utilities import Utilities

app = FastAPI()

# Post to "login" API endpoint
@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    # If the username exists AND the password is valid login
    if Utilities.verify_username_and_password(username, password):
        return {"message": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid username or password")

# Post to "tasks/{username} API endpoint"
@app.post("/tasks/{username}", response_model=dict)
# Add a task to the task list
async def add_task(username: str, task_name: str):
    task = Task(task_name, "", 1, "01/01/2024", 0, username)
    Utilities.add_task(task, username)
    return {"message": "Task added successfully."}

# Get from "tasks/{username} API endpoint"
@app.get("/tasks/{username}", response_model=List[dict])
async def get_tasks(username: str):
    task_list = Utilities.get_tasks(username)
    task_dicts = [task.to_dict() for task in task_list]
    return task_dicts


