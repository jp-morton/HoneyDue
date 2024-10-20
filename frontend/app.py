import streamlit as st
import requests

API_URL = "http://backend:8000"

# User authentication
def login(username, password):
    # Make call to the "login" API endpoint
    response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    return response.ok

# Main application
def main():
    # Main title
    st.title("HoneyDue")

    # LOGIN PAGE
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # If not logged in, display login page
    if not st.session_state.logged_in:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # If login pressed, log the user in 
        if st.button("Login"):
            # if login(username, password):
            if requests.post(f"{API_URL}/login", json={"username": username, "password": password}).ok:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
                st.success("Logged in successfully!")
                
            else:
                st.error("Invalid username or password")

    # TASKS PAGE
    else:
        st.subheader(f"Welcome, {st.session_state.username}")
        
        # Use columns for page layout
        col1, col2 = st.columns([3, 1])

        # COL1 OF TASKS PAGE
        if "tasks" not in st.session_state:
            st.session_state.tasks = []
        with col1:
            task_name = st.text_input("Enter a new task")
            
            if st.button("Add Task"):
                if task_name:
                    response = requests.post(f"{API_URL}/tasks/{st.session_state.username}", params={"username": st.session_state.username, "task_name": task_name})
                    if response.status_code == 200:
                        st.rerun()
                        st.success(f'Task "{task_name}" added!')
                    else:
                        st.error(f"Error: {response.text}")
                else:
                    st.error("Please enter a task.")

            # Fetch tasks
            st.subheader("Your Tasking")
            
            response = requests.get(f"{API_URL}/tasks/{st.session_state.username}", json={"username": st.session_state.username})
            if response.status_code == 200:
                task_list = response.json()
                i = 1
                for task in task_list:
                    st.write(f"{i}. {task['name']}")
                    i = i + 1

        # COL2 OF TASKS PAGE
        with col2:
            if st.button("Logout"): 
                # Reset session state, set states back to empty 
                st.session_state.clear()
                
                # Redirect to login page
                st.rerun()
                st.success("You have been logged out.")

if __name__ == "__main__":
    main()
