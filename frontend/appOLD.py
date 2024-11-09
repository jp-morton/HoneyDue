import streamlit as st
import requests

API_URL = "http://backend:8000"

# Helper function to handle user login
def login(username, password):
    response = requests.post(f"{API_URL}/login", params={"username": username, "password": password})
    return response.ok

# Helper function to handle user signup
def signup(username, password):
    response = requests.post(f"{API_URL}/signup", params={"username": username, "password": password})
    return response

# Helper function to fetch user tasks
def fetch_tasks(username):
    response = requests.get(f"{API_URL}/tasks/{username}", params={"username": username})
    if response.ok:
        return response.json()
    return []

# Helper function to add a new task
def add_task(username, task_name):
    requests.post(f"{API_URL}/tasks/{username}", params={"username": username, "task_name": task_name})

# Function to display login form and handle login logic
def display_login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")
    
    # Add "Back" button to return to home page
    if st.button("Back"):
        st.session_state.page = "home"
        st.rerun()

# Function to display signup form and handle account creation
def display_signup():
    st.subheader("Sign Up")
    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    
    if st.button("Sign Up"):
        signup_attempt = signup(username, password)
        if signup_attempt.ok:
            st.success("Account created successfully! Please log in.")
        else:
            error_detail = signup_attempt.json().get("detail", "Error: ")
            st.error(error_detail)
    
    # Add "Back" button to return to home page
    if st.button("Back"):
        st.session_state.page = "home"
        st.rerun()

# Function to display projects and add new projects
def display_projects():
    st.subheader(f"Welcome, {st.session_state.username}")
    col1, col2 = st.columns([3, 1])

    # COL1 OF HOME PAGE
    with col1:
        project_name = st.text_input("Enter a new project name")
        
        if st.button("Create Project"):
            if project_name:
                # THIS NEEDS TO BE IMPLEMENTED
                response = requests.post(f"{API_URL}/{st.session_state.username}", params={"username": st.session_state.username, "project_name": project_name})
                if response.status_code == 200:
                    st.rerun()
                    st.success(f"Project {project_name} added!")
                else:
                    st.error("Project with this name already exists or invalid input.")
            else:
                st.error("Please enter a project name.")
        
        # Fetch current projects
        st.subheader("Your Projects")

        response = requests.get(f"{API_URL}/{st.session_state.username}", params={"username": st.session_state.username})
        if response.status_code == 200:
            project_list = response.json()
            i = 1
            for project in project_list:
                if st.button(f"{i}. {project}"):
                    st.session_state.project_name = project
                    st.rerun()
                i = i + 1

    # COL2: Logout Button
    with col2:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()


# Function to display tasks and add new tasks
def display_tasks():
    st.subheader(f"{st.session_state.project_name} Homepage")
    # col1, col2, col3, col4, col5 = st.columns([3, 2, 5, 3, 4])
    col1, col2, col3 = st.columns([3, 2, 5])

    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/role", params={"project_name": st.session_state.project_name})
    if response.status_code == 200:
        role = response.json()

    # COL1 OF TASKS PAGE
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    with col1:
        # Add tasks (FOR MEMBER AND OWNER ONLY)
        if role != 'Guest':
            task_name = st.text_input("Enter a new task")
            
            if st.button("Add Task"):
                if task_name:
                    response = requests.post(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}", params={"username": st.session_state.username, "project_name": st.session_state.project_name, "task_name": task_name})
                    if response.status_code == 200:
                        st.rerun()
                        st.success(f'Task "{task_name}" added!')
                    else:
                        st.error(f"Error: {response.text}")
                else:
                    st.error("Please enter a task.")

        # Fetch tasks
        st.subheader("Project Tasks")
            
        response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}", params={"project_name": st.session_state.project_name})
        if response.status_code == 200:
            task_list = response.json()
            i = 1
            for task in task_list:
                st.write(f"{i}. {task['name']}")
                i = i + 1

    # COL2: Back and Logout buttons
    with col2:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

        if st.button("Back"):
            del st.session_state.project_name
            st.rerun()
    
    # COL3: Team Settings Button
    with col3:
        if st.button("Team Settings"):
            st.session_state["team_settings"] = True
            st.rerun()
    
# Function to display team settings
def display_team_settings():

    col1, col2 = st.columns([4, 2])
    with col1:
        st.title(st.session_state.project_name + " Team Settings")
    with col2:
        # Return button
        if st.button("Return"):
            del st.session_state["team_settings"]
            st.rerun()

    # Team Member List
    st.subheader("Team Members")
    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/collaborators", params={"project_name": st.session_state.project_name})
    if response.status_code == 200:
        collaborator_dict = response.json()
        for collaborator, role in collaborator_dict.items():
            st.write(f"{collaborator} : {role}")


    # OWNER ONLY
    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/role", params={"project_name": st.session_state.project_name})
    if response.status_code == 200:
        role = response.json()

    if role == 'Owner':
        st.subheader("Add Collaborator")

        # Add Collaborators 
        col1, col2, col3 = st.columns(3)
        with col1:
            username_entry = st.text_input("Username: ")

        with col2:
            user_role = st.selectbox('Role:', ('Select a role', 'Owner', 'Member', 'Guest'))
        
        with col3:
            if st.button('Add'):
                if user_role != 'Select a role':
                    if username_entry:
                        response = requests.post(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/collaborators", params={"collaborator_name": username_entry, "role": user_role, "project_name": st.session_state.project_name})
                        if response.status_code == 200:
                            st.rerun()
                            st.success(f'User "{username_entry}" added!')
                        else:
                            error_detail = response.json().get("detail", "Error: ")
                            st.error(error_detail)
                    else:
                        st.error("Please enter a username.")
                else:
                    st.error("Please select a role.")

        # Update Role
        st.subheader("Update Collaborator Role")
        col1, col2, col3 = st.columns(3)

        with col1:
            response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/collaborators", params={"project_name": st.session_state.project_name})
            if response.status_code == 200:
                collaborator_dict = response.json()
                collaborator_list = list(collaborator_dict.keys())
                collaborator_list.remove(st.session_state.username)
                collaborator = st.selectbox(f"Collaborator", ["Select a collaborator"] + collaborator_list)

        with col2:
            new_role = st.selectbox('Role', ('Select a role', 'Owner', 'Member', 'Guest'))

        with col3:
            if st.button(f'Update'):
                if new_role != 'Select a role':
                    if collaborator != 'Select a collaborator':
                        response = requests.post(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/role", params={"project_name": st.session_state.project_name, "collaborator": collaborator, "new_role": new_role})
                        if response.status_code == 200:
                            st.rerun()
                            st.success(f"Role has been updated.")
                        else:
                            st.error(f"Error: {response.text}")
                    else:
                        st.error("Please select a collaborator.")
                else:
                    st.error("Please select a role.")
    
        # Remove Collaborator
        st.subheader("Remove Collaborator")
        col1, col2 = st.columns(2)

        with col1:
            response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/collaborators", params={"project_name": st.session_state.project_name})
            if response.status_code == 200:
                collaborator_dict = response.json()
                collaborator_list = list(collaborator_dict.keys())
                collaborator_list.remove(st.session_state.username)
                collaborator = st.selectbox(f"Collaborator to remove", ["Select a collaborator"] + collaborator_list)
        
        with col2:
            if st.button("Remove"):
                if collaborator != 'Select a collaborator':
                    response = requests.post(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/remove_collaborator", params={"project_name": st.session_state.project_name, "collaborator": collaborator})
                    if response.status_code == 200:
                        st.rerun()
                        st.success(f"User has been removed.")
                    else:
                        st.error(f"Error: {response.text}")
                else:
                    st.error("Please select a collaborator.")

# Home page to choose between login or signup
def display_home():
    st.title("Welcome to HoneyDue")
    st.subheader("Please choose an option")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login"):
            st.session_state.page = "login"
            st.rerun()

    with col2:
        if st.button("Sign Up"):
            st.session_state.page = "signup"
            st.rerun()

# Main application
def main():
    st.title("HoneyDue")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "page" not in st.session_state:
        st.session_state.page = "home"

    # Navigation logic based on page state
    if "project_name" in st.session_state:
        if "team_settings" in st.session_state:
            display_team_settings()
        else:
            display_tasks()
    elif st.session_state.logged_in:
        display_projects()
    elif st.session_state.page == "home":
        display_home()
    elif st.session_state.page == "login":
        display_login()
    elif st.session_state.page == "signup":
        display_signup()

if __name__ == "__main__":
    main()