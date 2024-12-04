from enum import Enum

class Role(Enum):
    """
    Enum representing user roles in a project.

    Attributes:
        OWNER: Indicates the user owns the project and has full permissions.
        MEMBER: Indicates the user is a regular member of the project with standard permissions.
        GUEST: Indicates the user has limited permissions in the project.
    """
    OWNER = 'Owner'
    MEMBER = 'Member'
    GUEST = 'Guest'

class User:
    """
    A class used to represent a user.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
        projects (dict): A dictionary mapping project names to the user's role in each project.
    """

    def __init__(self, name, password):
        """
        Initializes a User instance.

        Args:
            name (str): The username of the user.
            password (str): The password for the user's account.
        """
        self.username = name
        self.password = password
        self.projects = {}
