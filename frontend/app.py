import streamlit as st
import requests

API_URL = "http://backend:8000"

# User authentication
def login(username, password):
    response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    return response.ok

# Main application
def main():
    st.title("HoneyDue")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password")
    else:
        st.subheader(f"Welcome, {st.session_state.username}")

        if "tasks" not in st.session_state:
            st.session_state.tasks = []

        task = st.text_input("Enter a new task")
        if st.button("Add Task"):
            if task:
                requests.post(f"{API_URL}/tasks/{st.session_state.username}", json={"task": task})
                st.session_state.tasks.append(task)
                st.success(f'Task "{task}" added!')
            else:
                st.error("Please enter a task.")

        # Fetch tasks
        if st.session_state.tasks == []:
            response = requests.get(f"{API_URL}/tasks/{st.session_state.username}")
            st.session_state.tasks = response.json()

        st.subheader("Your Tasks")
        for idx, task in enumerate(st.session_state.tasks):
            st.write(f"{idx + 1}. {task}")

if __name__ == "__main__":
    main()
