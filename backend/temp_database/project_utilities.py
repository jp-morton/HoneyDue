import h5py
import numpy as np
import pickle

from libraries.task import Task
from libraries.project import Project
from temp_database.account_utilities import Account_Utilities

class Project_Utilities:

    # Name: add_project
    # Description: Creates a dataset for the Project object
    # Input:
    #   project: The project object being added to the data
    def add_project(project: Project):
        with h5py.File('/app/temp_database/project_data.hdf5', 'a') as project_data:
            serialized_project = pickle.dumps(project)
            project_data.create_dataset(project.name, data=np.void(serialized_project))

    # Name: project_exists
    # Description: Checks to see if a project exists
    # Input:
    #   project_name: The project name being searched for
    # Output:
    #   True if the project name already exists
    #   False if the project name does not already exist
    def project_exists(project_name: str):
        with h5py.File('/app/temp_database/project_data.hdf5', 'a') as project_data:
            for project in project_data:
                if project == project_name:
                    return True
            return False

    # Name: add_collaborator
    # Description: adds a collaborator to a particular project
    # Input: 
    #   username: The username being added to the project member list
    #   project_name: The name of the project that the user is being added to 
    def add_collaborator(username: str, role: str, project_name: str):
        with h5py.File('/app/temp_database/project_data.hdf5', 'a') as project_data:
            if project_name not in project_data:
                raise ValueError(f"Project '{project_name}' not found.")
            try:
                serialized_project = project_data[project_name][()]
                project_obj = pickle.loads(serialized_project)
            except:
                raise ValueError(f"Error loading project '{project_name}'")
            project_obj.add_collaborator(username, role)
            # project_obj.members.append(username)
            serialized_project = pickle.dumps(project_obj)
            del project_data[project_name]
            project_data.create_dataset(project_name, data=np.void(serialized_project))

            Account_Utilities.add_project(project_name, username)

    # Name: get_collaborators
    # Description: Gets the list of collaborator names for a particular project
    # Input: 
    #   project_name: The name of the project whose collaborators are being retrieved
    # Output: 
    #   The list of collaborators
    def get_collaborators(project_name: str):
        with h5py.File('/app/temp_database/project_data.hdf5', 'r') as project_data:
            serialized_project = project_data[project_name][()]
            project_obj = pickle.loads(serialized_project)
            return project_obj.collaborators

    # Name: add_task
    # Description: Adds a task to a particular project
    # Input: 
    #   task: The Task object being added to the project 
    #   project_name: The name of the project that the task is being added to 
    def add_task(task: Task, project_name: str):
        with h5py.File('/app/temp_database/project_data.hdf5', 'a') as project_data:
            if project_name not in project_data:
                raise ValueError(f"Project '{project_name}' not found.")

            try:
                serialized_project = project_data[project_name][()]
                project_obj = pickle.loads(serialized_project)
            except:
                raise ValueError(f"Error loading project '{project_name}'")
            
            project_obj.tasks.append(task)
            serialized_project = pickle.dumps(project_obj)
            del project_data[project_name]
            project_data.create_dataset(project_name, data=np.void(serialized_project))

    # Name: get_task_list
    # Description: Retrieves the list of tasks for a particular project
    # Input
    #   project_name: The name of the project whose task list is being retrieved
    def get_task_list(project_name: str):
        with h5py.File('/app/temp_database/project_data.hdf5', 'r') as project_data:
            serialized_project = project_data[project_name][()]
            project_obj = pickle.loads(serialized_project)
            return project_obj.tasks

    # Name: get_project_owner
    # Description: Retrieves the username of the project owner
    # Input
    #   project_name: The name of the project whose owner is being retrieved 
    def get_project_owner(project_name: str):
        with h5py.File('/app/temp_database/project_data.hdf5', 'r') as project_data:
            serialized_project = project_data[project_name][()]
            project_obj = pickle.loads(serialized_project)
            return project_obj.owner

    # Name: get_user_role
    # Description: Returns a user's role in a particular project
    # Input
    #   project_name: the name of the project being searched
    #   username: The username of the user whose role is being retrieved
    # Output: The role (OWNER, MEMBER, GUEST) of the user for the specified project
    def get_user_role(project_name: str, username: str):
        if Account_Utilities.user_has_project(username, project_name):
            with h5py.File('/app/temp_database/project_data.hdf5', 'r') as project_data:
                serialized_project = project_data[project_name][()]
                project_obj = pickle.loads(serialized_project)
                return project_obj.collaborators[username]
        else:
            raise ValueError(f"User '{username}' is not in project {project_name}.")

    # Name: update_user_role
    # Description: Changes a user's role for a particular project
    # Input
    #   project_name: The name of the project that the role change is occurring in 
    #   username: The username of the user whose role is changing
    #   new_role: The new role (OWNER, MEMBER, GUEST) of the user
    def update_user_role(project_name: str, username: str, new_role: str):
        if Account_Utilities.user_has_project(username, project_name):
            with h5py.File('/app/temp_database/project_data.hdf5', 'a') as project_data:
                serialized_project = project_data[project_name][()]
                project_obj = pickle.loads(serialized_project)
                project_obj.update_role(username, new_role)
                serialized_project = pickle.dumps(project_obj)
                del project_data[project_name]
                project_data.create_dataset(project_name, data=np.void(serialized_project))
        else:
            raise ValueError(f"User '{username}' is not in project {project_name}.")

    # Name: remove_collaborator
    # Description: Removes a user as a collaborator for a project
    # Input:
    #   project_name: The name of the project that the user is being removed from 
    #   collaborator: The username of the user being removed
    def remove_collaborator(project_name: str, collaborator: str):
        with h5py.File('/app/temp_database/project_data.hdf5', 'a') as project_data:
            if project_name not in project_data:
                raise ValueError(f"Project '{project_name}' not found.")
            try:
                serialized_project = project_data[project_name][()]
                project_obj = pickle.loads(serialized_project)
            except:
                raise ValueError(f"Error loading project '{project_name}'")
            project_obj.remove_collaborator(collaborator)
            serialized_project = pickle.dumps(project_obj)
            del project_data[project_name]
            project_data.create_dataset(project_name, data=np.void(serialized_project))

            Account_Utilities.remove_project(project_name, collaborator)
