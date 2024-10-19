import streamlit as st
import requests

API_URL = "http://backend:8000"

# Helper function to handle user login
def login(username, password):
    response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    return response.ok

# Helper function to handle user signup
def signup(username, password):
    response = requests.post(f"{API_URL}/signup", json={"username": username, "password": password})
    return response.ok

# Helper function to fetch user tasks
def fetch_tasks(username):
    response = requests.get(f"{API_URL}/tasks/{username}")
    if response.ok:
        return response.json()
    return []

# Helper function to add a new task
def add_task(username, task):
    requests.post(f"{API_URL}/tasks/{username}", json={"task": task})

# Function to display login form and handle login logic
def display_login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.tasks = fetch_tasks(username)  # Fetch tasks upon login
            st.rerun()
        else:
            st.error("Invalid username or password")

# Function to display signup form and handle account creation
def display_signup():
    st.subheader("Sign Up")
    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    
    if st.button("Sign Up"):
        if signup(username, password):
            st.success("Account created successfully! Please log in.")
        else:
            st.error("Username already exists or invalid input.")

# Function to display tasks and add new tasks
def display_tasks():
    st.subheader(f"Welcome, {st.session_state.username}")
    col1, col2 = st.columns([3, 1])

    # COL1: Task input and display
    with col1:
        task = st.text_input("Enter a new task")
        if st.button("Add Task"):
            if task:
                add_task(st.session_state.username, task)
                st.session_state.tasks.append(task)
                st.rerun()
            else:
                st.error("Please enter a task.")

        # Display task list
        st.subheader("Your Tasks")
        for idx, task in enumerate(st.session_state.tasks):
            st.write(f"{idx + 1}. {task}")

    # COL2: Logout button
    with col2:
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
    if st.session_state.logged_in:
        display_tasks()
    elif st.session_state.page == "home":
        display_home()
    elif st.session_state.page == "login":
        display_login()
    elif st.session_state.page == "signup":
        display_signup()

if __name__ == "__main__":
    main()
