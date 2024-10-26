import h5py
import numpy as np
import pickle
import base64

from libraries.task import Task
from libraries.project import Project

class Utilities:

    ######################
    ### USER FUNCTIONS ###
    ######################

    # Name: find_username
    # Description: Searches the account data to see if a username has been used
    # Input: 
    #   username: The username being searched for
    # Output:
    #   True if the username is found
    #   False if the username is not found
    def find_username(username: str):
        with h5py.File('/app/temp_database/account_data.hdf5', 'r') as account_data:
            for user in account_data:
                user_group = account_data[user]
                if user_group.attrs['Username'] == username:
                    return True
            return False

    # Name: find_password
    # Description: Searches the account data to see if a password has been used
    # Input: 
    #   password: The password being searched for
    # Output:
    #   True if the password is found
    #   False if the password is not found
    def find_password(password: str):
        with h5py.File('/app/temp_database/account_data.hdf5', 'r') as account_data:
            for user in account_data:
                user_group = account_data[user]
                if user_group.attrs['Password'] == password:
                    return True
            return False

    # Name: find_username_and_password
    # Description: Searches the account data to see if an account exists 
    # Input: 
    #   username: The username of the account being searched for
    #   password: The password of the account being searched for
    # Output:
    #   True if the account is found
    #   False if the account is not found
    def find_username_and_password(username: str, password: str):
        with h5py.File('/app/temp_database/account_data.hdf5', 'r') as account_data:
            for user in account_data:
                user_group = account_data[user]
                if user_group.attrs['Username'] == username and user_group.attrs['Password'] == password:
                    return True
            return False
    
    # Name: add_user
    # Description: Add a new user to the account data
    # Input: 
    #   username: The username of the user being added
    #   password: The password of the user being added 
    def add_user(username: str, password: str):
        with h5py.File('/app/temp_database/account_data.hdf5', 'a') as account_data:
            user_group = account_data.create_group(f'User_{len(account_data) + 1}')
            user_group.attrs['Username'] = username
            user_group.attrs['Password'] = password
            user_group.create_dataset('Projects', shape=(0,), maxshape=(None,), dtype=h5py.special_dtype(vlen=str))

    #########################
    ### PROJECT FUNCTIONS ###
    #########################

    # Name: add_project
    # Description: Add a new project to a user's account data
    # Input: 
    #   project: The Project object being added
    #   username: The username of the user adding the project
    def add_project(project: Project, username: str):
        with h5py.File('/app/temp_database/account_data.hdf5', 'a') as account_data:
            for user in account_data:
                user_group = account_data[user]
                if user_group.attrs['Username'] == username:
                    project_dataset = user_group['Projects']
                    serialized_project = pickle.dumps(project, protocol=pickle.HIGHEST_PROTOCOL)
                    encoded_project = base64.b64encode(serialized_project).decode('utf-8')
                    project_dataset.resize(project_dataset.shape[0] + 1, axis=0)
                    project_dataset[-1] = encoded_project

    # Name: get_projects
    # Description: Retrieve the list of projects for a particular user
    # Input: 
    #   username: The username of the User whose projects are being retrieved
    # Output: 
    #   The list of the user's projects
    def get_projects(username: str):
        with h5py.File('/app/temp_database/account_data.hdf5', 'r') as account_data:
            for user in account_data:
                user_group = account_data[user]
                if user_group.attrs['Username'] == username:
                    project_dataset = user_group['Projects']
                    project_list = [pickle.loads(base64.b64decode(encoded_project)) for encoded_project in project_dataset]
                    return project_list                    
    
    # Name: project_exists
    # Description: Check to see if a project already exists with a particular name
    # Input: 
    #   username: The username of the user whose projects are being searched
    #   project_name: The project name being searched for 
    def project_exists(username: str, project_name: str):
        with h5py.File('/app/temp_database/account_data.hdf5', 'a') as account_data:
            for user in account_data:
                user_group = account_data[user]
                if user_group.attrs['Username'] == username: # and 'Projects' in user_group:
                    project_dataset = user_group['Projects']
                    project_list = [pickle.loads(base64.b64decode(encoded_project)) for encoded_project in project_dataset]
                    for project in project_list:
                        if project.name == project_name:
                            return True
                    return False
            return False


    ######################
    ### TASK FUNCTIONS ###
    ######################

    # Name: add_task
    # Description: Add a new task for a particular project
    # Input: 
    #   task: The Task object being added to the project
    #   username: The username of user adding the task
    #   project_name: The name of the project that the task is being added to 
    def add_task(task: Task, username: str, project_name: str):
        with h5py.File('/app/temp_database/account_data.hdf5', 'a') as account_data:
            for user in account_data:
                user_group = account_data[user]
                if user_group.attrs['Username'] == username:
                    project_dataset = user_group['Projects']
                    project_list = [pickle.loads(base64.b64decode(encoded_project)) for encoded_project in project_dataset]

                    for project in project_list:
                        if project.name == project_name:
                            project.add_task(task)
                            serialized_project = pickle.dumps(project, protocol=pickle.HIGHEST_PROTOCOL)
                            encoded_project = base64.b64encode(serialized_project).decode('utf-8')
                            project_dataset[-1] = encoded_project

    # Name: get_tasks
    # Description: Retrieve the list of tasks for a particular project
    # Input: 
    #   username: The username of the user whose tasks are being retrieved
    #   project_name: The name of the project whose tasks are being retrieved
    # Output:
    #   List of tasks for a particular project
    def get_tasks(username: str, project_name: str):
        with h5py.File('/app/temp_database/account_data.hdf5', 'r') as account_data:
            for user in account_data:
                user_group = account_data[user]
                if user_group.attrs['Username'] == username:
                    project_dataset = user_group['Projects']
                    project_list = [pickle.loads(base64.b64decode(encoded_project)) for encoded_project in project_dataset]
                    for project in project_list:
                        if project.name == project_name:
                            return project.tasks
