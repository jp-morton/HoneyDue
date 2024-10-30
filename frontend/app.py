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
    return response.ok

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
        # if login(username, password):
        if requests.post(f"{API_URL}/login", params={"username": username, "password": password}).ok:
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
        if signup(username, password):
            st.success("Account created successfully! Please log in.")
        else:
            st.error("Username or Password already exists or invalid input.")
    
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
            # for project in project_list:
            #     st.write(f"{i}. {project['name']}")
            #     i = i + 1
            for project in project_list:
                if st.button(f"{i}. {project['name']}"):
                    # st.write(f"{project['name']} was clicked")
                    st.session_state.project_name = project['name']
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
    col1, col2, col3 = st.columns([3, 1, 1])

    # COL1 OF TASKS PAGE
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    with col1:
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
        st.subheader("Your Tasks")
            
        response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}", params={"username": st.session_state.username, "project_name": st.session_state.project_name})
        if response.status_code == 200:
            task_list = response.json()
            i = 1
            for task in task_list:
                st.write(f"{i}. {task['name']}")
                i = i + 1

    # COL2: Back button
    with col2:
        if st.button("Back"):
            del st.session_state.project_name
            st.rerun()
    
    # COL3: Logout button
    with col3:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

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
