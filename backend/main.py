from fastapi import FastAPI, HTTPException, Request

from typing import List

from libraries.task import Task
from libraries.project import Project
from utilities.account_utilities import Account_Utilities
from utilities.project_utilities import Project_Utilities

app = FastAPI()

# IF SET TO TRUE, THE FOLLOWING FLAG WILL RESET THE DATABASE 
database_reset = True
if database_reset:
    Account_Utilities.reset()
    Project_Utilities.reset()

# Sign up route
@app.post("/signup")
def signup(username: str, password: str):
    try:
        Account_Utilities.add_user(username, password)
        return {"message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")

# Post to "login" API endpoint
@app.post("/login")
async def login(username: str, password: str):
    # If the username exists AND the password is valid login
    if Account_Utilities.account_exists(username, password):
        return {"message": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid username or password")

# Post to "{username} API endpoint"
@app.post("/{username}", response_model=dict)
async def add_project(username: str, project_name: str):
    if Project_Utilities.project_exists(project_name):
        raise HTTPException(status_code=400, detail="Project name already exists")
    else:
        project = Project(project_name, username)
        Account_Utilities.add_project(project_name, username)
        Project_Utilities.add_project(project)
        return {"message": "Project added successfully."}


# Get from "{username} API endpoint"
@app.get("/{username}", response_model = List[str])
async def get_projects(username: str):
    project_list = Account_Utilities.get_project_list(username)
    return project_list

# Post to "{username}/{project_name}/task API endpoint"
@app.post("/{username}/{project_name}/task", response_model=dict)
# Add a task to the task list
async def add_task(request: Request):
    task_info = await request.json()
    new_task = Task(
        name=task_info.get("task_name"), 
        description=task_info.get("description"), 
        priority=task_info.get("priority"),
        deadline=task_info.get("deadline"),
        category=task_info.get("category"),
        status=task_info.get("status"),
        assignee=task_info.get("assignee")
    )
    Project_Utilities.add_task(new_task, task_info.get("project_name"))
    return {"message": "Task added successfully."}

# Get from "{username}/{project_name}/task API endpoint"
@app.get("/{username}/{project_name}/task", response_model=List[dict])
async def get_tasks(project_name: str):
    task_list = Project_Utilities.get_task_list(project_name)
    task_dicts = [task.to_dict() for task in task_list]
    return task_dicts

# Post to "{username}/{project_name}/category API endpoint"
@app.post("/{username}/{project_name}/category", response_model=dict)
# Add a category to the category list
async def add_category(project_name: str, category_name: str):

    if Project_Utilities.category_exists(category_name, project_name):
        raise HTTPException(status_code=400, detail="Category already exists")
    else:
        Project_Utilities.add_category(category_name, project_name)
        return {"message": "Category added successfully."}

# Get from "{username}/{project_name}/category API endpoint"
@app.get("/{username}/{project_name}/category", response_model=list)
async def get_categories(project_name: str):
    category_list = Project_Utilities.get_category_list(project_name)
    return category_list

# Post to "{username}/{project_name}/task_updates API endpoint"
@app.post("/{username}/{project_name}/task_updates", response_model=dict)
# Update the tasks
async def update_tasks(request: Request):
    body = await request.json()
    project_name = body['project_name']
    updated_tasks = body['updated_tasks']
    Project_Utilities.update_task_list(project_name, updated_tasks)
    return {"message": "Tasks updated successfully."}

# Post to "{username}/{project_name}/category_updates API endpoint"
@app.post("/{username}/{project_name}/remove_category", response_model=dict)
# Update the categories
async def remove_category(project_name: str, category: str):
    
    Project_Utilities.remove_category(project_name, category)
    return {"message": "Category removed successfully."}


# Post to "{username}/{project_name}/collaborators API endpoint"
@app.post("/{username}/{project_name}/collaborators", response_model=dict)
# Add a collaborator
async def add_collaborator(collaborator_name: str, role: str, project_name: str):
    if Account_Utilities.username_exists(collaborator_name):
        if not Account_Utilities.user_has_project(collaborator_name, project_name):
            Project_Utilities.add_collaborator(collaborator_name, role, project_name)
            return {"message": "User added successfully."}
        else:
            raise HTTPException(status_code=400, detail=f"{collaborator_name} is already a collaborator")
    else:
        raise HTTPException(status_code=400, detail=f"{collaborator_name} does not exist")

# Post to "{username}/{project_name}/collaborators API endpoint"
@app.get("/{username}/{project_name}/collaborators", response_model = dict)
# Get collaborator dict
async def get_collaborators(project_name: str):
    collaborator_dict = Project_Utilities.get_collaborators(project_name)
    return collaborator_dict

# Post to "{username}/{project_name}/role API endpoint"
@app.post("/{username}/{project_name}/role", response_model=dict)
async def update_user_role(project_name: str, collaborator: str, new_role: str):
    Project_Utilities.update_user_role(project_name, collaborator, new_role)
    return {"message": "User role updated successfully."}

# Get from "{username}/{project_name}/role API endpoint"
@app.get("/{username}/{project_name}/role", response_model=str)
async def get_user_role(project_name: str, username: str):
    role = Project_Utilities.get_user_role(project_name, username)
    return role

# Post to "{username}/{project_name}/remove_collaborator API endpoint"
@app.post("/{username}/{project_name}/remove_collaborator")
async def remove_collaborator(project_name: str, collaborator: str):
    Project_Utilities.remove_collaborator(project_name, collaborator)
    return {"message": "User role updated successfully."}
