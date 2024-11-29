import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
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
    # Display button organization
    col1, col2, col3 = st.columns([6, 1, 1])
    with col1:
        st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")


    col4, col5 = st.columns([4, 3])
    with col4:
        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password")

    # Move "Home" button to top right
    with col3:    
        # Add "Home" button to return to home page
        if st.button("Home"):
            st.session_state.page = "home"
            st.rerun()

    with col2:
        # Add "Sign up" button to login screen
        if st.button("Sign up"):
            st.session_state.page = "signup"
            st.rerun()


# Function to display signup form and handle account creation
def display_signup():

    col1, col2, col3 = st.columns([6, 1, 0.9])
    with col1:
        st.subheader("Sign Up")
    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    verify_password = st.text_input("Verify Password", type="password")
    
    col4, col5 = st.columns([4, 3])

    with col4:
        if st.button("Sign Up"):
            signup_attempt = signup(username, password, verify_password)
            if password == verify_password:
                if signup_attempt.ok:
                    st.success("Account created successfully! Please log in.")
            else:
                error_detail = signup_attempt.json().get("detail", "Error: ")
                st.error(error_detail)

    with col2:
        # Add "Home" button to return to home page
        if st.button("Home"):
            st.session_state.page = "home"
            st.rerun()

    with col3:    
        # Add "Back" button to return to previous page
        if st.button("Login"):
            st.session_state.page = "login"
            st.rerun()

# Function to display projects and add new projects
def display_projects():
    st.subheader(f"Welcome, {st.session_state.username}")
    col1, col2 = st.columns([3, 1])

    # COL1 OF HOME PAGE
    with col1:
        project_name = st.text_input("Enter a new project name")
        
        # Create a project
        if st.button("Create Project"):
            if project_name:
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

    col1, col2 = st.columns(2)

    # COL1: Back and Logout buttons
    with col1:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

        if st.button("Back"):
            del st.session_state.project_name
            st.rerun()

    # COL2: Team Settings button
    with col2:
        if st.button("Team Settings"):
            st.session_state["team_settings"] = True
            st.rerun()
        if st.button("Manage Tasks"):
            st.session_state["task_list"] = True
            st.rerun()


    col1, col2, col3 = st.columns(3)

    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/role", params={"project_name": st.session_state.project_name})
    if response.status_code == 200:
        role = response.json()

    with col1:
        # CALENDAR PLACEHOLDER
        calendar()


    # COL2 OF TASKS PAGE
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    with col2:
        # Add tasks (FOR MEMBER AND OWNER ONLY)
        if role != 'Guest':
            with st.expander("Add Task"):
                task_name = st.text_input("Task Name")
                task_description = st.text_area("Task Description", value="None")
                priority = st.number_input("Priority", min_value=1, max_value=5, value=1)
                deadline = st.date_input("Deadline")

                response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/category", params={"project_name": st.session_state.project_name})
                if response.status_code == 200:
                    category_list = response.json()
                    category = st.selectbox(f"Category", category_list)

                status = st.selectbox("Task Status", options=["TODO", "DOING", "DONE"])

                response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/collaborators", params={"project_name": st.session_state.project_name})
                if response.status_code == 200:
                    collaborator_dict = response.json()
                    collaborator_list = list(collaborator_dict.keys())
                    collaborator_list.remove(st.session_state.username)
                    assignee = st.selectbox(f"Assignee", ["Assign to me"] + collaborator_list)

                
                if st.button("Add Task"):
                    if not task_name:
                        st.error("Please enter a task name")
                    elif not task_description:
                        st.error("Please enter a task description")
                    else:
                        if assignee == "Assign to me":
                            assignee = st.session_state.username

                        task_data = {
                            "project_name": st.session_state.project_name,
                            "task_name": task_name, 
                            "description": task_description, 
                            "priority": str(priority), 
                            "deadline": deadline.isoformat(), 
                            "category": category, 
                            "status": status, 
                            "assignee": assignee
                        }

                        response = requests.post(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/task", json=task_data)
                        if response.status_code == 200:
                            st.rerun()
                            st.success(f'Task "{task_name}" added!')
                        else:
                            st.error(f"Error: {response.text}")
    
    with col3:
        # Add categories (FOR MEMBER AND OWNER ONLY)
        if role != 'Guest':
            with st.expander("Add Category"):
                category_name = st.text_input("Category Name")

                if st.button("Add Category"):
                    if category_name:
                        if category_name not in category_list:
                            response = requests.post(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/category", params={"project_name": st.session_state.project_name, "category_name": category_name})
                            if response.status_code == 200:
                                st.rerun()
                                st.success(f'Category "{category_name}" added!')
                            else:
                                st.error(response.text)
                        else:
                            st.error(f"Category '{category_name}' already exists")
                    else:
                        st.error("Please enter a name")

def display_task_list():
    # Back button
    if st.button("Back"):
        del st.session_state["task_list"]
        st.rerun()
    
    st.subheader("Tasks")

    # Get user role
    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/role", params={"project_name": st.session_state.project_name})
    if response.status_code == 200:
        role = response.json()

    # Get task list
    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/task", params={"project_name": st.session_state.project_name})
    if response.status_code == 200:
        task_list = response.json()
        
    # Get category list
    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/category", params={"project_name": st.session_state.project_name})
    if response.status_code == 200:
        category_list = response.json()
        filtered_category_list = category_list.copy()
        filtered_category_list.remove("None")

    # OWNER AND MEMBER ONLY
    if role != "Guest":

        # List of Assignees
        response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/collaborators", params={"project_name": st.session_state.project_name})
        if response.status_code == 200:
            collaborator_dict = response.json()
            collaborator_list = list(collaborator_dict.keys())
        
        # Create dataframe
        df = pd.DataFrame(task_list)
        status_order = ["TODO", "DOING", "DONE"]
        df["status"] = pd.Categorical(df["status"], categories=status_order, ordered=True)
        df["deadline"] = pd.to_datetime(df["deadline"])

        column_config = {
            "priority": st.column_config.SelectboxColumn(label="Task Priority", options=["1", "2", "3", "4", "5"],),
            "category": st.column_config.SelectboxColumn(label="Category", options=category_list,),
            "status": st.column_config.SelectboxColumn(label="Status", options=status_order),
            "assignee": st.column_config.SelectboxColumn(label="Assignee", options=collaborator_list),
            "deadline": st.column_config.DateColumn(label="Deadline"),
        }

        sort_by = st.selectbox("Sort Tasks", options=df.columns.tolist(), index=0)
        sort_order = st.radio("Task order", options=["Ascending", "Descending"], index=0)
        ascending = True if sort_order == "Ascending" else False
        df_sorted = df.sort_values(by=sort_by, ascending=ascending)
        df_sorted_reset = df_sorted.reset_index(drop=True)

        edited_df = st.data_editor(df_sorted_reset, num_rows="dynamic", column_config=column_config, use_container_width=True)

        # Update button
        if st.button("Update Tasks"):
            if edited_df is not None and not df_sorted_reset.equals(edited_df):
                if edited_df.isnull().values.any() or (edited_df == "").values.any():
                    st.error("All fields must be filled before updating")
                else:
                    edited_df["deadline"] = edited_df["deadline"].dt.strftime('%Y-%m-%d')
                    payload = {
                        "updated_tasks": edited_df.to_dict(orient="records"),
                        "project_name": st.session_state.project_name
                    }
                    
                    update_response = requests.post(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/task_updates", json=payload)
                    if update_response.status_code == 200:
                        st.rerun()
                        st.success("Data updated successfully")
                    else:
                        st.error(f"Failed to update data. Status code: {update_response.status_code}")
            else:
                st.warning("No changes were made to the tasks")

    # GUEST ONLY
    else:
        # Task dataframe
        st.dataframe(task_list, use_container_width=True)

    # Category Management
    st.subheader("Categories")

    i = 1
    for category in filtered_category_list:
        st.write(f"{i}. {category}")
        i = i + 1

    if role != "Guest":
        col1, col2 = st.columns(2)

        with col1:
            category_entry = st.text_input("Category: ")
        
        with col2:
            if st.button('Add'):
                if category_entry:
                    if category_entry in category_list:
                        st.error(f"Category '{category_entry}' already exists")
                    else:
                        response = requests.post(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/category", params={"project_name": st.session_state.project_name, "category_name": category_entry})
                        if response.status_code == 200:
                            st.rerun()
                            st.success(f'Category "{category_entry}" added!')
                        else:
                            st.error("There was an error adding the category")
                else:
                    st.error("Please enter a category name")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_category = st.selectbox(f"Category", ["Select a category"] + filtered_category_list)

        with col2:
            if st.button("Remove"):
                if selected_category != 'Select a category':
                    response = requests.post(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/remove_category", params={"project_name": st.session_state.project_name, "category": selected_category})
                    if response.status_code == 200:
                        st.rerun()
                        st.success(f"Category has been removed.")
                    else:
                        st.error(f"Error: {response.text}")
                else:
                    st.error("Please select a category.")

# Function to display team settings
def display_team_settings():

    col1, col2 = st.columns([4, 2])
    with col1:
        st.title(st.session_state.project_name + " Team Settings")
    with col2:
        # Back button
        if st.button("Back"):
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

    #Adjusting the 'Welcome to HoneyDue' to the center of the page. 
    st.markdown(
        """
        <style>
        .centered-title {
            text-align: center;
            font-size: 3em; /* Adjust font size as needed */
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="centered-title">Welcome to HoneyDue! </div>', unsafe_allow_html=True)

    #Centered the buttons to the screen
    col1, col2, col3 = st.columns([.60,.50,1])
    
    with col2:
        if st.button("Login"):
            st.session_state.page = "login"
            st.rerun()

    with col3:
        if st.button("Sign Up"):
            st.session_state.page = "signup"
            st.rerun()

# Main application
def main():

    #Displaying the background image

    #Each screen will have the HoneyDue sign on the top
    st.markdown(
        """
        <style>
        .header-title {
            font-size: 8em; /* Larger font size */
            font-weight: bold;
            text-align: center;
            padding: 10px; /* Space around the title */             
        }
        </style>
        """,
        unsafe_allow_html=True
    )   
    st.markdown('<div class="header-title">HoneyDue</div>', unsafe_allow_html=True)
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "page" not in st.session_state:
        st.session_state.page = "home"

    # Navigation logic based on page state
    if "project_name" in st.session_state:
        if "team_settings" in st.session_state:
            display_team_settings()
        elif "task_list" in st.session_state:
            display_task_list()
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

# test

if __name__ == "__main__":
    main()
