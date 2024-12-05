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

# Post to signup a user 
@app.post("/signup")
def signup(username: str, password: str):
    """
    Endpoint for user signup.

    Args:
        username (str): The username of the new user.
        password (str): The password for the new user.

    Returns:
        dict: A success message if the user is created successfully.

    Raises:
        HTTPException: Returns a 400 status code if an error occurs during user creation,
                       with the error message in the detail field.
    """
    try:
        Account_Utilities.add_user(username, password)
        return {"message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")

@app.post("/login")
async def login(username: str, password: str):
    """
    Endpoint for user login.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The password of the user attempting to log in.

    Returns:
        dict: A success message if the username exists and the password is valid.

    Raises:
        HTTPException: Returns a 400 status code with a message indicating 
                       invalid credentials if the login attempt fails.
    """
    if Account_Utilities.account_exists(username, password):
        return {"message": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid username or password")

@app.post("/{username}", response_model=dict)
async def add_project(username: str, project_name: str):
    """
    Endpoint to add a new project for a specified user.

    Args:
        username (str): The username of the account to which the project will be added.
        project_name (str): The name of the project to be created and associated with the user.

    Returns:
        dict: A success message if the project is added successfully.

    Raises:
        HTTPException: Returns a 400 status code with a message if the project name 
                       already exists.
    """
    if Project_Utilities.project_exists(project_name):
        raise HTTPException(status_code=400, detail="Project name already exists")
    else:
        project = Project(project_name, username)
        Account_Utilities.add_project(project_name, username)
        Project_Utilities.add_project(project)
        return {"message": "Project added successfully."}

@app.get("/{username}", response_model = List[str])
async def get_projects(username: str):
    """
    Endpoint to retrieve the list of projects associated with a specified user.

    Args:
        username (str): The username whose project list is being requested.

    Returns:
        List[str]: A list of project names associated with the given username.
    """
    project_list = Account_Utilities.get_project_list(username)
    return project_list

@app.post("/{username}/delete_project")
async def delete_project(project_name: str):
    """
    Endpoint to delete a project. 

    Args:
        project_name (str): The name of the project to be deleted.
    
    Returns:
        dict: A JSON response with a success message if the project is deleted successfully.
    
    Raises:
        HTTPException: Occurs if the project does not exist or if an error occurs during deletion 
    """
    try:
        collaborator_list = Project_Utilities.get_collaborators(project_name)
        if Project_Utilities.project_exists(project_name):
            Project_Utilities.delete_project(project_name)

            for user in collaborator_list.keys():
                Account_Utilities.delete_project(project_name, user)
            return {"message": "Project removed successfully"}
    except:
        raise HTTPException(status_code=400, detail="An error occured while deleting the project.")

# Post to "{username}/{project_name}/task API endpoint"
@app.post("/{username}/{project_name}/task", response_model=dict)
async def add_task(request: Request):
    """
    Endpoint to add a new task to a specified project.

    Args:
        request (Request): The HTTP request object containing the task details in JSON format.

    Request Body:
        JSON object with the following keys:
        - task_name (str): Name of the task.
        - description (str): Description of the task.
        - priority (str): Priority level of the task (1-5).
        - deadline (str): Deadline for task completion (format: YYYY-MM-DD).
        - category (str): Category or type of task.
        - status (str): Current status of the task (TODO, DOING, DONE).
        - assignee (str): Name of the person assigned to the task.
        - project_name (str): Name of the project to which the task is being added.

    Returns:
        dict: A dictionary containing a success message.
    """
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

@app.get("/{username}/{project_name}/task", response_model=List[dict])
async def get_tasks(project_name: str):
    """
    Endpoint to retrieve the list of tasks for a specified project.

    Args:
        project_name (str): The name of the project for which tasks are to be retrieved.

    Returns:
        List[dict]: A list of dictionaries, where each dictionary represents a task and contains task details such as:
        - name (str): Task name.
        - description (str): Task description.
        - priority (str): Priority level of the task (1-5).
        - deadline (str): Deadline for the task (format: YYYY-MM-DD).
        - category (str): Category or type of task.
        - status (str): Current status of the task (TODO, DOING, DONE).
        - assignee (str): Name of the person assigned to the task.

    Raises:
        HTTPException: Could be added for cases where the project does not exist.
    """
    task_list = Project_Utilities.get_task_list(project_name)
    task_dicts = [task.to_dict() for task in task_list]
    return task_dicts

@app.post("/{username}/{project_name}/category", response_model=dict)
async def add_category(project_name: str, category_name: str):
    """
    Endpoint to add a new category to a specific project.

    Args:
        project_name (str): The name of the project to which the category will be added.
        category_name (str): The name of the category to be added.

    Returns:
        dict: A success message indicating that the category was added.

    Raises:
        HTTPException (status_code=400): If the category already exists for the specified project.
    """
    if Project_Utilities.category_exists(category_name, project_name):
        raise HTTPException(status_code=400, detail="Category already exists")
    else:
        Project_Utilities.add_category(category_name, project_name)
        return {"message": "Category added successfully."}

@app.get("/{username}/{project_name}/category", response_model=list)
async def get_categories(project_name: str):
    """
    Endpoint to retrieve a list of categories for a specific project.

    Args:
        project_name (str): The name of the project whose categories are being retrieved.

    Returns:
        list: A list of category names associated with the given project.
    """
    category_list = Project_Utilities.get_category_list(project_name)
    return category_list

@app.post("/{username}/{project_name}/task_updates", response_model=dict)
async def update_tasks(request: Request):
    """
    Endpoint to update the task list for a specific project.

    Args:
        request (Request): The HTTP request containing the JSON body with updated tasks.

    Returns:
        dict: A success message indicating the task list was updated.
    """
    body = await request.json()
    project_name = body['project_name']
    updated_tasks = body['updated_tasks']
    Project_Utilities.update_task_list(project_name, updated_tasks)
    return {"message": "Tasks updated successfully."}

@app.post("/{username}/{project_name}/remove_category", response_model=dict)
async def remove_category(project_name: str, category: str):
    """
    Endpoint to remove a specific category from a project.

    Args:
        project_name (str): The name of the project where the category exists.
        category (str): The name of the category to be removed.

    Returns:
        dict: A success message indicating the category was removed.
    """
    Project_Utilities.remove_category(project_name, category)
    return {"message": "Category removed successfully."}


@app.post("/{username}/{project_name}/collaborators", response_model=dict)
async def add_collaborator(collaborator_name: str, role: str, project_name: str):
    """
    Endpoint to add a collaborator to a project with a specific role.

    Args:
        collaborator_name (str): The username of the collaborator to add.
        role (str): The role to assign to the collaborator.
        project_name (str): The name of the project to which the collaborator is being added.

    Returns:
        dict: A success message if the collaborator is added successfully.

    Raises:
        HTTPException: If the collaborator does not exist or is already part of the project.
    """
    if Account_Utilities.username_exists(collaborator_name):
        if not Account_Utilities.user_has_project(collaborator_name, project_name):
            Project_Utilities.add_collaborator(collaborator_name, role, project_name)
            return {"message": "User added successfully."}
        else:
            raise HTTPException(status_code=400, detail=f"{collaborator_name} is already a collaborator")
    else:
        raise HTTPException(status_code=400, detail=f"{collaborator_name} does not exist")

@app.get("/{username}/{project_name}/collaborators", response_model = dict)
async def get_collaborators(project_name: str):
    """
    Endpoint to retrieve a dictionary of collaborators for a project.

    Args:
        project_name (str): The name of the project whose collaborators are being retrieved.

    Returns:
        dict: A dictionary containing collaborator names and their roles for the specified project.
    """
    collaborator_dict = Project_Utilities.get_collaborators(project_name)
    return collaborator_dict

@app.post("/{username}/{project_name}/role", response_model=dict)
async def update_user_role(project_name: str, collaborator: str, new_role: str):
    """
    Endpoint to update a collaborator's role in a project.

    Args:
        project_name (str): The name of the project where the collaborator is assigned.
        collaborator (str): The username of the collaborator whose role is being updated.
        new_role (str): The new role to assign to the collaborator.

    Returns:
        dict: A success message indicating the role update.
    """
    Project_Utilities.update_user_role(project_name, collaborator, new_role)
    return {"message": "User role updated successfully."}

@app.get("/{username}/{project_name}/role", response_model=str)
async def get_user_role(project_name: str, username: str):
    """
    Endpoint to retrieve the role of a specific user in a project.

    Args:
        project_name (str): The name of the project.
        username (str): The username of the user whose role is being retrieved.

    Returns:
        str: The role of the specified user in the project.
    """
    role = Project_Utilities.get_user_role(project_name, username)
    return role

@app.post("/{username}/{project_name}/remove_collaborator")
async def remove_collaborator(project_name: str, collaborator: str):
    """
    Endpoint to remove a collaborator from a project.

    Args:
        project_name (str): The name of the project.
        collaborator (str): The username of the collaborator to remove.

    Returns:
        dict: A success message indicating the collaborator was removed.
    """
    Project_Utilities.remove_collaborator(project_name, collaborator)
    return {"message": "User role updated successfully."}
