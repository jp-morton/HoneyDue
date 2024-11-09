import h5py

class Account_Utilities:

    #################################
    ### SIGN UP / LOGIN FUNCTIONS ###
    #################################

    # Name: username_exists
    # Description: Searches the account data to see if a username has been used
    # Input: 
    #   username: The username being searched for
    # Output:
    #   True if the username is found
    #   False if the username is not found        
    def username_exists(username: str):
        with h5py.File('/app/database/account_data.hdf5', 'r') as account_data:
            if username in account_data:
                return True
            return False

    # Name: password_exists
    # Description: Searches the account data to see if a password has been used
    # Input: 
    #   password: The password being searched for
    # Output:
    #   True if the password is found
    #   False if the password is not found
    def password_exists(password: str):
        with h5py.File('/app/database/account_data.hdf5', 'r') as account_data:
            for user in account_data:
                user_group = account_data[user]
                if user_group.attrs['Password'] == password:
                    return True
            return False

    # Name: account_exists
    # Description: Searches the account data to see if an account exists 
    # Input: 
    #   username: The username of the account being searched for
    #   password: The password of the account being searched for
    # Output:
    #   True if the account is found
    #   False if the account is not found
    def account_exists(username: str, password: str):
        with h5py.File('/app/database/account_data.hdf5', 'r') as account_data:
            try:
                user_group = account_data[username]
                if user_group.attrs['Password'] == password:
                    return True
                return False
            except:
                return False

    # Name: add_user
    # Description: Add a new user to the account data. Will raise an error if the username or password already exists
    # Input: 
    #   username: The username of the user being added
    #   password: The password of the user being added 
    def add_user(username: str, password: str):
        with h5py.File('/app/database/account_data.hdf5', 'a') as account_data:
            if Account_Utilities.username_exists(username):  
                raise ValueError("Username already exists.")
            elif Account_Utilities.password_exists(password):
                raise ValueError("Password already exists.")
            else:
                user_group = account_data.create_group(username)
                user_group.attrs['Password'] = password
                user_group.create_dataset('Projects', shape=(0,), maxshape=(None,), dtype=h5py.string_dtype(encoding='utf-8'))

    #########################
    ### PROJECT FUNCTIONS ###
    #########################

    # Name: user_has_project
    # Description: Check to see if a user has a project with a particular name 
    # Input: 
    #   username: The username whose projects are being checked
    #   project_name: The name of the project being searched for
    # Output: 
    #   True if the user does have the project
    #   False if the user does not have the project 
    def user_has_project(username: str, project_name: str):
        project_list = Account_Utilities.get_project_list(username)
        if project_name in project_list:
            return True
        else:
            return False

    # Name: add_project
    # Description: Add a new project to a user's account data
    # Input: 
    #   project_name: The name of the project being added
    #   username: The username of the user adding the project
    def add_project(project_name: str, username: str):

        with h5py.File('/app/database/account_data.hdf5', 'a') as account_data:
            try:
                user_group = account_data[username]
                project_dataset = user_group['Projects']
                project_dataset.resize((project_dataset.shape[0] + 1,))
                project_dataset[-1] = project_name.encode('utf-8')
            except:
                raise ValueError(f"There was an error adding Project {project_name} to {username}")
            
    # Name: remove_project
    # Description: Removes a project name from the user's project list
    # Input: 
    #   project_name: The name of the project being removed
    #   username: The name of the user who is having the project removed 
    def remove_project(project_name: str, username: str):

        with h5py.File('/app/database/account_data.hdf5', 'a') as account_data:
            try:
                user_group = account_data[username]
                project_dataset = user_group['Projects']
                project_list = [p.decode('utf-8') for p in project_dataset[()]]

                if project_name in project_list:
                    project_list.remove(project_name)

                    del user_group['Projects']
                    user_group.create_dataset('Projects', shape=(0,), maxshape=(None,), dtype=h5py.string_dtype(encoding='utf-8'))
                    for project in project_list:
                        Account_Utilities.add_project(project, username)
            except:
                raise ValueError(f"User {username} or project dataset does not exist")

    # Name: get_project_list
    # Description: Retrieve the list of project names for a particular user
    # Input: 
    #   username: The username of the User whose projects are being retrieved
    # Output: 
    #   The list of the user's projects
    def get_project_list(username: str):
        with h5py.File('/app/database/account_data.hdf5', 'r') as account_data:
            for user in account_data:
                if user == username:
                    user_group = account_data[user]
                    project_dataset = user_group['Projects']
                    project_list = [project.decode('utf-8') for project in project_dataset]
                    return project_list
