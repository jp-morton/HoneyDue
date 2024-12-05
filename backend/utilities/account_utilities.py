import bcrypt
import h5py

class Account_Utilities:
    """
    A utility class for managing accounts and associated project data stored in an HDF5 file.

    Methods:
        username_exists(username): Check if a username exists in the database.
        password_exists(password): Check if a password exists in the database.
        account_exists(username, password): Check if an account with the given credentials exists.
        add_user(username, password): Add a new user to the database.
        user_has_project(username, project_name): Check if a user has a specific project.
        add_project(project_name, username): Add a project to a user's project list.
        delete_project(project_name, username): Remove a project from a user's project list.
        get_project_list(username): Retrieve a list of projects for a user.
        reset(): Reset the database to default values (used for testing).
    """

    #################################
    ### SIGN UP / LOGIN FUNCTIONS ###
    #################################

    @staticmethod
    def username_exists(username: str):
        """
        Check if a username exists in the database.

        Args:
            username (str): The username to search for.

        Returns:
            bool: True if the username exists, False otherwise.
        """
        with h5py.File('/app/database/account_data.hdf5', 'r') as account_data:
            if username in account_data:
                return True
            return False

    @staticmethod
    def password_exists(password: str):
        """
        Check if a password exists in the database.

        Args:
            password (str): The password to search for.

        Returns:
            bool: True if the password exists, False otherwise.
        """
        with h5py.File('/app/database/account_data.hdf5', 'r') as account_data:
            for user in account_data:
                user_group = account_data[user]
                stored_hash = user_group.attrs['Password']
                
                if isinstance(stored_hash, str): 
                    stored_hash = stored_hash.encode('utf-8')
                
                password_encoded = password.encode('utf-8')

                try:
                    if bcrypt.checkpw(password_encoded, stored_hash):
                        return True
                except TypeError as e:
                    print(f"Error checking password: {e}")
                    return False
            return False

    @staticmethod
    def account_exists(username: str, password: str):
        """
        Check if an account exists with the given username and password.

        Args:
            username (str): The username of the account.
            password (str): The password of the account.

        Returns:
            bool: True if the account exists, False otherwise.
        """
        with h5py.File('/app/database/account_data.hdf5', 'r') as account_data:
            try:
                user_group = account_data[username]
                stored_hash = user_group.attrs['Password']
                
                if isinstance(stored_hash, str):
                    stored_hash = stored_hash.encode('utf-8')

                password_encoded = password.encode('utf-8')
                
                if bcrypt.checkpw(password_encoded, stored_hash):
                    return True
                return False
            except KeyError:
                return False

    @staticmethod
    def add_user(username: str, password: str):
        """
        Add a new user to the database.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.

        Raises:
            ValueError: If the username or password already exists.
        """
        with h5py.File('/app/database/account_data.hdf5', 'a') as account_data:
            if Account_Utilities.username_exists(username):  
                raise ValueError("Username already exists.")
            elif Account_Utilities.password_exists(password):
                raise ValueError("Password already exists.")
            else:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                
                user_group = account_data.create_group(username)
                user_group.attrs['Password'] = hashed_password  
                user_group.create_dataset('Projects', shape=(0,), maxshape=(None,), dtype=h5py.string_dtype(encoding='utf-8'))

    #########################
    ### PROJECT FUNCTIONS ###
    #########################

    @staticmethod
    def user_has_project(username: str, project_name: str):
        """
        Check if a user has a specific project.

        Args:
            username (str): The username to check.
            project_name (str): The project name to look for.

        Returns:
            bool: True if the user has the project, False otherwise.
        """
        project_list = Account_Utilities.get_project_list(username)
        if project_name in project_list:
            return True
        else:
            return False

    @staticmethod
    def add_project(project_name: str, username: str):
        """
        Add a new project to a user's project list.

        Args:
            project_name (str): The name of the project.
            username (str): The username of the user.

        Raises:
            ValueError: If the project cannot be added.
        """
        with h5py.File('/app/database/account_data.hdf5', 'a') as account_data:
            try:
                user_group = account_data[username]
                project_dataset = user_group['Projects']
                project_dataset.resize((project_dataset.shape[0] + 1,))
                project_dataset[-1] = project_name.encode('utf-8')
            except:
                raise ValueError(f"There was an error adding Project {project_name} to {username}")

    @staticmethod
    def delete_project(project_name: str, username: str):
        """
        Remove a project from a user's project list.

        Args:
            project_name (str): The name of the project to remove.
            username (str): The username of the user.

        Raises:
            ValueError: If the user or project does not exist.
        """
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

    @staticmethod
    def get_project_list(username: str):
        """
        Retrieve the list of projects for a user.

        Args:
            username (str): The username of the user.

        Returns:
            list: A list of project names.
        """
        with h5py.File('/app/database/account_data.hdf5', 'r') as account_data:
            for user in account_data:
                if user == username:
                    user_group = account_data[user]
                    project_dataset = user_group['Projects']
                    project_list = [project.decode('utf-8') for project in project_dataset]
                    return project_list

    #################################################
    # THE FOLLOWING FUNCTION IS TO RESET THE DATABASE
    #################################################

    @staticmethod
    def reset():
        """
        Reset the database to default values for testing purposes.

        Creates default users and assigns one project to each user.
        """
        with h5py.File('/app/database/account_data.hdf5', 'w') as account_data:
            Account_Utilities.add_user('user1', 'password1')
            Account_Utilities.add_user('user2', 'password2')
            Account_Utilities.add_user('user3', 'password3')
            Account_Utilities.add_user('user4', 'password4')

        Account_Utilities.add_project('Project1', 'user1')
        Account_Utilities.add_project('Project2', 'user2')
        Account_Utilities.add_project('Project3', 'user3')
        Account_Utilities.add_project('Project4', 'user4')
