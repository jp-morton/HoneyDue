from fastapi import FastAPI, HTTPException, Request

from pydantic import BaseModel
from typing import List
import uvicorn
import h5py
import numpy as np

from libraries.user import User
from libraries.task import Task
from libraries.project import Project
from temp_database.data_utilities import Utilities

app = FastAPI()




# Sign up route
@app.post("/signup")
def signup(username: str, password: str):
    if Utilities.username_exists(username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if Utilities.password_exists(password):
        raise HTTPException(status_code=400, detail="Password already exists")
    # Hash the password and store the user
    # hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    # users_db[user.username] = hashed_password
    Utilities.add_user(username, password)
    # users_db[user.username] = user.password
    return {"message": "User created successfully"}


# Post to "login" API endpoint
@app.post("/login")
async def login(username: str, password: str):
    # If the username exists AND the password is valid login
    if Utilities.account_exists(username, password):
        return {"message": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid username or password")

# Post to "{username} API endpoint"
@app.post("/{username}", response_model=dict)
async def add_project(username: str, project_name: str):
    if Utilities.project_exists(username, project_name):
        raise HTTPException(status_code=400, detail="Project name already exists")
    project = Project(project_name, username)
    Utilities.add_project(project, username)
    return {"message": "Project added successfully."}


# Get from "{username} API endpoint"
@app.get("/{username}", response_model = List[dict])
async def get_projects(username: str):
    project_list = Utilities.get_project_list(username)
    project_dicts = [project.to_dict() for project in project_list]
    return project_dicts

# Post to "{username}/{project_name} API endpoint"
@app.post("/{username}/{project_name}", response_model=dict)
# Add a task to the task list
async def add_task(username: str, project_name: str, task_name: str):
    task = Task(task_name, "", 1, "01/01/2024", 0, username)
    Utilities.add_task(task, username, project_name)
    return {"message": "Task added successfully."}

# Get from "{username}/{project_name} API endpoint"
@app.get("/{username}/{project_name}", response_model=List[dict])
async def get_tasks(username: str, project_name: str):
    task_list = Utilities.get_task_list(username, project_name)
    task_dicts = [task.to_dict() for task in task_list]
    return task_dicts
