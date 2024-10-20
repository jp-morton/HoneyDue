import h5py
import numpy as np
import pickle

from libraries.task import Task

class Utilities:

    def verify_username_and_password(username: str, password: str):
        print("\nVerifying username and password")
        with h5py.File('/app/temp_database/account_data.hdf5', 'r') as account_data:
            for user in account_data:
                user_group = account_data[user]
                if user_group.attrs['Username'] == username and user_group.attrs['Password'] == password:
                    print("\nUser found\n")
                    return True
            return False

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
