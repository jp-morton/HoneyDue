import h5py
import numpy as np
import pickle

from libraries.task import Task

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


    ######################
    ### TASk FUNCTIONS ###
    ######################

    # Name: add_task
    # Description: Add a new task for a particular user
    # Input: 
    #   task: The Task object being added
    #   username: The username of the assignee of the task
    def add_task(task: Task, username: str):
        pickled_task = pickle.dumps(task)
        with h5py.File('/app/temp_database/account_data.hdf5', 'a') as account_data:
            for user in account_data:
                user_group = account_data[user]
                if user_group.attrs['Username'] == username:
                    if 'Tasks' not in user_group:
                        task_dataset = user_group.create_dataset('Tasks', shape=(0,), maxshape=(None,), dtype='S' + str(len(pickled_task)))
                    task_dataset = user_group['Tasks']
                    task_dataset.resize(task_dataset.shape[0] + 1, axis=0)
                    task_dataset[-1] = pickled_task

    # Name: get_tasks
    # Description: Retrieve the list of tasks for a particular user
    # Input: 
    #   username: The username of the user whose tasks are being retrieved
    def get_tasks(username: str):
        with h5py.File('/app/temp_database/account_data.hdf5', 'r') as account_data:
            for user in account_data:
                user_group = account_data[user]
                if user_group.attrs['Username'] == username:
                    if 'Tasks' not in user_group:
                        return []
                    task_dataset = user_group['Tasks']
                    retrieved_tasks = []
                    for task in task_dataset:
                        task_obj = pickle.loads(task)
                        retrieved_tasks.append(task_obj)
                    return retrieved_tasks
