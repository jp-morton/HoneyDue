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
            if login(username, password):
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
            task = st.text_input("Enter a new task")
            if st.button("Add Task"):
                if task:
                    requests.post(f"{API_URL}/tasks/{st.session_state.username}", json={"task": task})
                    st.session_state.tasks.append(task)
                    st.rerun()
                    st.success(f'Task "{task}" added!')
                else:
                    st.error("Please enter a task.")

            # Fetch tasks
            if st.session_state.tasks == []:
                response = requests.get(f"{API_URL}/tasks/{st.session_state.username}")
                st.session_state.tasks = response.json()

            # Display task list as enumeration
            st.subheader("Your Tasks")
            for idx, task in enumerate(st.session_state.tasks):
                st.write(f"{idx + 1}. {task}")

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
