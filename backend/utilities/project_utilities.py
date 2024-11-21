import h5py
import numpy as np
import pickle

from libraries.task import Task
from libraries.project import Project
from utilities.account_utilities import Account_Utilities

class Project_Utilities:

    # Name: add_project
    # Description: Creates a dataset for the Project object
    # Input:
    #   project: The project object being added to the data
    def add_project(project: Project):
        with h5py.File('/app/database/project_data.hdf5', 'a') as project_data:
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
        with h5py.File('/app/database/project_data.hdf5', 'a') as project_data:
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
        with h5py.File('/app/database/project_data.hdf5', 'a') as project_data:
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
        with h5py.File('/app/database/project_data.hdf5', 'r') as project_data:
            serialized_project = project_data[project_name][()]
            project_obj = pickle.loads(serialized_project)
            return project_obj.collaborators

    # Name: add_task
    # Description: Adds a task to a particular project
    # Input: 
    #   task: The Task object being added to the project 
    #   project_name: The name of the project that the task is being added to 
    def add_task(task: Task, project_name: str):
        with h5py.File('/app/database/project_data.hdf5', 'a') as project_data:
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
        with h5py.File('/app/database/project_data.hdf5', 'r') as project_data:
            serialized_project = project_data[project_name][()]
            project_obj = pickle.loads(serialized_project)
            return project_obj.tasks

    # Name: add_category
    # Description: Adds a category to a particular project
    # Input: 
    #   task: The name of the category being added to the project 
    #   project_name: The name of the project that the category is being added to 
    def add_category(category_name: str, project_name: str):
        with h5py.File('/app/database/project_data.hdf5', 'a') as project_data:
            if project_name not in project_data:
                raise ValueError(f"Project '{project_name}' not found.")

            try:
                serialized_project = project_data[project_name][()]
                project_obj = pickle.loads(serialized_project)
            except:
                raise ValueError(f"Error loading project '{project_name}'")

            project_obj.categories.append(category_name)
            serialized_project = pickle.dumps(project_obj)
            del project_data[project_name]
            project_data.create_dataset(project_name, data=np.void(serialized_project))

    # Name: get_category_list
    # Description: Retrieves the list of categories for a particular project
    # Input
    #   project_name: The name of the project whose category list is being retrieved
    def get_category_list(project_name: str):
        with h5py.File('/app/database/project_data.hdf5', 'r') as project_data:
            serialized_project = project_data[project_name][()]
            project_obj = pickle.loads(serialized_project)
            return project_obj.categories

    # Name: category_exists
    # Description: Checks to see if a category exists
    # Input:
    #   category_name: The category name being searched for
    #   project_name: The project being searched in
    # Output:
    #   True if the category already exists
    #   False if the category does not already exist
    def category_exists(category_name: str, project_name: str):
        category_list = Project_Utilities.get_category_list(project_name)
        for category in category_list:
            if category_name == category:
                return True
        return False
    
    # Name: update_task_list
    # Description: Updates a project's task list 
    # Input: 
    #   project_name: The name of the project whose tasks are being updated
    #   task_list: A list of dictionaries, each of which contain the contents of a task object in the project
    def update_task_list(project_name: str, task_list: list[dict]):
        with h5py.File('/app/database/project_data.hdf5', 'a') as project_data:
            if project_name not in project_data:
                raise ValueError(f"Project '{project_name}' not found.")

            try:
                serialized_project = project_data[project_name][()]
                project_obj = pickle.loads(serialized_project)
            except:
                raise ValueError(f"Error loading project '{project_name}'")
            
            project_obj.tasks = []
            for task in task_list:
                task_obj = Task(
                    name=task.get('name'), 
                    description=task.get('description'),
                    priority=task.get('priority'), 
                    deadline=task.get('deadline'), 
                    category=task.get('category'),
                    status=task.get('status'),
                    assignee=task.get('assignee')
                )
                project_obj.tasks.append(task_obj)

            serialized_project = pickle.dumps(project_obj)
            del project_data[project_name]
            project_data.create_dataset(project_name, data=np.void(serialized_project))

    # Name: remove_category
    # Description: Deletes a category from a project 
    # Input: 
    #   project_name: The name of the project whose category is being deleted
    #   category_name: The name of the category being deleted
    def remove_category(project_name: str, category_name: str):
        with h5py.File('/app/database/project_data.hdf5', 'a') as project_data:
            if project_name not in project_data:
                raise ValueError(f"Project '{project_name}' not found.")

            try:
                serialized_project = project_data[project_name][()]
                project_obj = pickle.loads(serialized_project)
            except:
                raise ValueError(f"Error loading project '{project_name}'")
            
            for task in project_obj.tasks:
                if task.category == category_name:
                    task.category = "None"

            project_obj.remove_category(category_name)

            serialized_project = pickle.dumps(project_obj)
            del project_data[project_name]
            project_data.create_dataset(project_name, data=np.void(serialized_project))

    # Name: get_user_role
    # Description: Returns a user's role in a particular project
    # Input
    #   project_name: the name of the project being searched
    #   username: The username of the user whose role is being retrieved
    # Output: The role (OWNER, MEMBER, GUEST) of the user for the specified project
    def get_user_role(project_name: str, username: str):
        if Account_Utilities.user_has_project(username, project_name):
            with h5py.File('/app/database/project_data.hdf5', 'r') as project_data:
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
            with h5py.File('/app/database/project_data.hdf5', 'a') as project_data:
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
        with h5py.File('/app/database/project_data.hdf5', 'a') as project_data:
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





    #################################################
    # THE FOLLOWING FUNCTION IS TO RESET THE DATABASE
    #################################################

    def reset():
        project_data = h5py.File('/app/database/project_data.hdf5', 'w')

        #################
        ### PROJECT 1 ###
        #################
        Project1 = Project('Project1', 'user1')
        Project_Utilities.add_project(Project1)

        # Add collaborators to project 1
        Project_Utilities.add_collaborator('user2', 'Member', 'Project1')
        Project_Utilities.add_collaborator('user3', 'Member', 'Project1')
        Project_Utilities.add_collaborator('user4', 'Guest', 'Project1')

        # Add categories to project 1
        Project_Utilities.add_category("Category1", 'Project1')
        Project_Utilities.add_category("Category2", 'Project1')
        Project_Utilities.add_category("Category3", 'Project1')

        # Add tasks to project 1
        task1 = Task(name="Task1", description="This is a test task called Task1 in None", priority=2, deadline="2024-12-25", category="None", status="TODO", assignee="user1")
        task2 = Task(name="Task2", description="This is a test task called Task2 in Category1", priority=3, deadline="2024-12-21", category="Category1", status="DONE", assignee="user2")
        task3 = Task(name="Task3", description="This is a test task called Task3 in Category1", priority=1, deadline="2025-01-04", category="Category1", status="TODO", assignee="user3")
        task4 = Task(name="Task4", description="This is a test task called Task4 in Category2", priority=4, deadline="2025-01-11", category="Category2", status="TODO", assignee="user1")
        task5 = Task(name="Task5", description="This is a test task called Task5 in Category2", priority=5, deadline="2024-12-15", category="Category2", status="DOING", assignee="user3")
        task6 = Task(name="Task6", description="This is a test task called Task6 in Category3", priority=2, deadline="2025-12-31", category="Category3", status="DOING", assignee="user2")

        Project_Utilities.add_task(task1, 'Project1')
        Project_Utilities.add_task(task2, 'Project1')
        Project_Utilities.add_task(task3, 'Project1')
        Project_Utilities.add_task(task4, 'Project1')
        Project_Utilities.add_task(task5, 'Project1')
        Project_Utilities.add_task(task6, 'Project1')

        #################
        ### PROJECT 2 ###
        #################
        Project2 = Project('Project2', 'user2')
        Project_Utilities.add_project(Project2)

        # Add collaborators to project 2
        Project_Utilities.add_collaborator('user1', 'Member', 'Project2')
        Project_Utilities.add_collaborator('user3', 'Owner', 'Project2')
        Project_Utilities.add_collaborator('user4', 'Member', 'Project2')

        # Add categories to project 2
        Project_Utilities.add_category("Cat1", 'Project2')
        Project_Utilities.add_category("Cat2", 'Project2')
        Project_Utilities.add_category("Cat3", 'Project2')

        # Add tasks to project 2
        task1 = Task(name="Task1", description="This is a test task called Task1", priority=2, deadline="2024-12-25", category="Cat3", status="TODO", assignee="user1")
        task2 = Task(name="Task1", description="This is a test task called Task1", priority=3, deadline="2024-12-21", category="Cat3", status="DONE", assignee="user2")
        task3 = Task(name="Task1", description="This is a test task called Task1", priority=1, deadline="2025-01-04", category="Cat2", status="TODO", assignee="user3")
        task4 = Task(name="Task1", description="This is a test task called Task1", priority=4, deadline="2025-01-11", category="Cat1", status="TODO", assignee="user1")
        task5 = Task(name="Task2", description="This is a test task called Task2", priority=5, deadline="2024-12-15", category="None", status="DOING", assignee="user3")
        task6 = Task(name="Task2", description="This is a test task called Task2", priority=2, deadline="2025-12-31", category="None", status="TODO", assignee="user4")

        Project_Utilities.add_task(task1, 'Project2')
        Project_Utilities.add_task(task2, 'Project2')
        Project_Utilities.add_task(task3, 'Project2')
        Project_Utilities.add_task(task4, 'Project2')
        Project_Utilities.add_task(task5, 'Project2')
        Project_Utilities.add_task(task6, 'Project2')

        #################
        ### PROJECT 3 ###
        #################
        Project3 = Project('Project3', 'user3')
        Project_Utilities.add_project(Project3)

        # Add collaborators to project 3
        Project_Utilities.add_collaborator('user1', 'Guest', 'Project3')
        Project_Utilities.add_collaborator('user2', 'Guest', 'Project3')
        Project_Utilities.add_collaborator('user4', 'Member', 'Project3')

        # Add categories to project 3
        Project_Utilities.add_category("C1", 'Project3')
        Project_Utilities.add_category("C2", 'Project3')
        Project_Utilities.add_category("C3", 'Project3')

        # Add tasks to project 3
        task1 = Task(name="Task1", description="This is a test task called Task1", priority=2, deadline="2024-12-25", category="C2", status="DOING", assignee="user4")
        task2 = Task(name="Task1", description="This is a test task called Task1", priority=3, deadline="2024-12-21", category="C2", status="TODO", assignee="user3")
        task3 = Task(name="Task1", description="This is a test task called Task1", priority=1, deadline="2025-01-04", category="C3", status="DONE", assignee="user3")
        task4 = Task(name="Task1", description="This is a test task called Task1", priority=4, deadline="2025-01-11", category="C3", status="DONE", assignee="user3")
        task5 = Task(name="Task2", description="This is a test task called Task2", priority=5, deadline="2024-12-15", category="None", status="TODO", assignee="user3")
        task6 = Task(name="Task2", description="This is a test task called Task2", priority=2, deadline="2025-12-31", category="C1", status="DOING", assignee="user4")

        Project_Utilities.add_task(task1, 'Project3')
        Project_Utilities.add_task(task2, 'Project3')
        Project_Utilities.add_task(task3, 'Project3')
        Project_Utilities.add_task(task4, 'Project3')
        Project_Utilities.add_task(task5, 'Project3')
        Project_Utilities.add_task(task6, 'Project3')

        #################
        ### PROJECT 4 ###
        #################
        Project4 = Project('Project4', 'user4')
        Project_Utilities.add_project(Project4)

        # Add collaborators to project 4
        Project_Utilities.add_collaborator('user1', 'Owner', 'Project4')
        Project_Utilities.add_collaborator('user2', 'Guest', 'Project4')
        Project_Utilities.add_collaborator('user3', 'Member', 'Project4')

        # Add categories to project 4
        Project_Utilities.add_category("Feature1", 'Project4')
        Project_Utilities.add_category("Feature2", 'Project4')
        Project_Utilities.add_category("Feature3", 'Project4')

        # Add tasks to project 4
        task1 = Task(name="Task1", description="This is a test task called Task1", priority=2, deadline="2024-12-25", category="Feature1", status="TODO", assignee="user4")
        task2 = Task(name="Task1", description="This is a test task called Task1", priority=3, deadline="2024-12-21", category="Feature1", status="DOING", assignee="user3")
        task3 = Task(name="Task1", description="This is a test task called Task1", priority=1, deadline="2025-01-04", category="Feature2", status="DONE", assignee="user1")
        task4 = Task(name="Task1", description="This is a test task called Task1", priority=4, deadline="2025-01-11", category="Feature2", status="DONE", assignee="user1")
        task5 = Task(name="Task2", description="This is a test task called Task2", priority=5, deadline="2024-12-15", category="Feature3", status="DONE", assignee="user4")
        task6 = Task(name="Task2", description="This is a test task called Task2", priority=2, deadline="2025-12-31", category="Feature3", status="TODO", assignee="user4")

        Project_Utilities.add_task(task1, 'Project4')
        Project_Utilities.add_task(task2, 'Project4')
        Project_Utilities.add_task(task3, 'Project4')
        Project_Utilities.add_task(task4, 'Project4')
        Project_Utilities.add_task(task5, 'Project4')
        Project_Utilities.add_task(task6, 'Project4')
