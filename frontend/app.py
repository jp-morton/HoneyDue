import streamlit as st
import streamlit.components.v1 as components
from streamlit_calendar import calendar
import pandas as pd
import requests
import pathlib

# Backend API URL
API_URL = "http://backend:8000"

# Function to load CSS from given path
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

# Load CSS to style the app
css_path = pathlib.Path("styles.css")
load_css(css_path)

# Display the web app logo 
st.logo("https://i.pinimg.com/originals/fe/be/ca/febeca2f63bd56c127069bac2fff9323.jpg", size="large")

# Function to handle user login
def login(username, password):
    response = requests.post(f"{API_URL}/login", params={"username": username, "password": password})
    return response.ok

# Function to handle user signup
def signup(username, password, verify_password):
    response = requests.post(f"{API_URL}/signup", params={"username": username, "password": password, "verify password": verify_password})
    return response

# Function to display login form and handle login logic
def display_login():

    display_company_logo()

    st.subheader("Login")
    with st.form("Login", clear_on_submit=True, border=False):
        # User inputs for username and password 
        username = st.text_input("Username", placeholder="Username", label_visibility="collapsed", key= 'goldInput1')
        password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed", key= 'goldInput2')

        # If the login button is selected 
        if st.form_submit_button("Login"):

            # User successfully logs in 
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
                st.success("Logged in successfully!")
            # Invalid entry  
            else:
                st.error("Invalid username or password")
    
    # Add "Back" button to return to home page
    if st.sidebar.button("Back", key = 'Back'):
        st.session_state.page = "home"
        st.rerun()

# Function to display signup form and handle account creation
def display_signup():

    display_company_logo()

    st.subheader("Sign Up")
    with st.form("Sign Up", clear_on_submit=True, border=False):
        # User inputs for username, password, and password verification 
        username = st.text_input("Create Username", placeholder= "New User", label_visibility="collapsed")
        password = st.text_input("Create Password", type="password", placeholder="Create Password", label_visibility="collapsed")
        verify_password = st.text_input("Confirm Password", type="password", placeholder="Confirm Password", label_visibility="collapsed")

        # Signup button is selected 
        if st.form_submit_button("Sign Up"):
            if verify_password == password:
                signup_attempt = signup(username, password, verify_password)
                if signup_attempt.ok:
                    st.success("Account created successfully! Please log in.")
                else:
                    st.error("Account with this username already exists.")
            else:
                st.error("Passwords mismatch")
    
    # Add "Back" button to return to home page
    if st.sidebar.button("Back", key = 'Back'):
        st.session_state.page = "home"
        st.rerun()
   
    # Add "Login" button to go to the login page
    if st.sidebar.button("Login", key = 'Login'):
        st.session_state.page = "login"
        st.rerun()

# Function to display projects and add new projects
def display_projects():

    display_company_logo()

    col1, col2, col3 = st.columns([5, 5, 5])
    st.session_state.disabled = False

    with col2:
        st.subheader(f"Welcome, {st.session_state.username}!")
        with st.form("New Project", clear_on_submit=True, border=False):
            # Project name entry 
            project_name = st.text_input("Enter a new project name", placeholder="New Project", label_visibility="collapsed")

            # If "Create Project" button is selected
            if st.form_submit_button("Create Project"):
                if project_name:
                    response = requests.post(f"{API_URL}/{st.session_state.username}", params={"username": st.session_state.username, "project_name": project_name})
                    if response.status_code == 200:
                        st.rerun()
                        st.success(f"Project {project_name} added!")
                    else:
                        st.error("Project with this name already exists or invalid input.")
                else:
                    st.error("Please enter a project name.")
   
   # If logout button is selected, return to the login/signup page 
    if st.sidebar.button("Logout", key = 'Logout'):
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")

    with st.sidebar:    
        # Fetch current projects
        st.subheader("Your Projects")

        response = requests.get(f"{API_URL}/{st.session_state.username}", params={"username": st.session_state.username})
        if response.status_code == 200:
            project_list = response.json()
            i = 1
            for project in project_list:
                # Add a button for each project 
                if st.button(f"{i}. {project}"):
                    st.session_state.project_name = project
                    st.rerun()
                i = i + 1

# Function to display project view 
def display_tasks():
    st.subheader(f"{st.session_state.project_name} Homepage")

    # Logout button 
    if st.sidebar.button("Logout", key= 'Logout'):
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")

    # Button to return back to list of projects 
    if st.sidebar.button("Back", key= 'Back'):
        del st.session_state.project_name
        st.rerun()

    # Team settings button 
    if st.sidebar.button("Team Settings", key= 'TeamSet'):
            st.session_state["team_settings"] = True
            st.rerun()

    # Button to view and manage list of tasks and categories 
    if st.sidebar.button("Manage Tasks", key= 'TaskMan'):
        st.session_state["task_list"] = True
        st.rerun()

    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/role", params={"project_name": st.session_state.project_name})
    if response.status_code == 200:
        role = response.json()

    # CALENDAR PLACEHOLDER
    calendar()

# Function to display task management page 
def display_task_list():

    # Logout button
    if st.sidebar.button("Logout", key= 'Logout'):
        st.session_state.clear()
        st.rerun()
    
    st.sidebar.markdown("---")
        
    # Back button to return to project view 
    if st.sidebar.button("Back", key= 'Back'):
        del st.session_state["task_list"]
        st.rerun()
    
    col1, col2 = st.columns(2)

    # Get the user roles for the project 
    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/role", params={"project_name": st.session_state.project_name})
    if response.status_code == 200:
        role = response.json()

    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    with col1:
        # Add tasks (FOR MEMBER AND OWNER ONLY)
        if role != 'Guest':
            with st.form("Add Task", clear_on_submit=True, border=False):
                with st.expander("Add Tasks"):
                    task_name = st.text_input("Task Name", placeholder="Task Name", label_visibility="collapsed")
                    task_description = st.text_area("Task Description", placeholder="Task Description", label_visibility="collapsed")
                    priority = st.number_input("Priority", min_value=1, max_value=5, value=1)
                    deadline = st.date_input("Deadline")

                    # Get category list 
                    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/category", params={"project_name": st.session_state.project_name})
                    if response.status_code == 200:
                        category_list = response.json()
                        category = st.selectbox(f"Category", category_list, index=None, placeholder="Category", label_visibility="collapsed")

                    # Status selection 
                    status = st.selectbox("Task Status", options=["TODO", "DOING", "DONE"], index=None, placeholder="Task Status", label_visibility= "collapsed")

                    # Get collaborator list 
                    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/collaborators", params={"project_name": st.session_state.project_name})
                    if response.status_code == 200:
                        collaborator_dict = response.json()
                        collaborator_list = list(collaborator_dict.keys())
                        collaborator_list.remove(st.session_state.username)
                        assignee = st.selectbox(f"Assignee", ["Assign to me"] + collaborator_list, index=None, placeholder="Assign To" ,label_visibility="collapsed")

                    # Button to create the task 
                    if st.form_submit_button("Add Task"):
                        if not task_name:
                            st.error("Please enter a task name")
                        elif not task_description:
                            st.error("Please enter a task description")
                        else:
                            if assignee == "Assign to me":
                                assignee = st.session_state.username

                            # Get task data for the API 
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

                        # Send the task data to the backend 
                        response = requests.post(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/task", json=task_data)
                        if response.status_code == 200:
                            st.rerun()
                            st.success(f'Task "{task_name}" added!')
                        else:
                            st.error(f"Error: {response.text}")

        # Creating a category (OWNER AND MEMBER ONLY)
        if role != "Guest":
            
            with st.sidebar.form("Add", clear_on_submit=True, border=False):

                    category_entry = st.text_input("Category: ", placeholder="Category", label_visibility="collapsed" )

                    # Button to create a new category 
                    if st.form_submit_button("Add"):
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
        
        # Get task list
        response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/task", params={"project_name": st.session_state.project_name})
        if response.status_code == 200:
            task_list = response.json()

    # Task table for MEMBERS and OWNERS
    if len(task_list) != 0 and role != "Guest":        
        # Get category list
        response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/category", params={"project_name": st.session_state.project_name})
        if response.status_code == 200:
            category_list = response.json()
            filtered_category_list = category_list.copy()
            filtered_category_list.remove("None")

        # Get list of assignees
        response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/collaborators", params={"project_name": st.session_state.project_name})
        if response.status_code == 200:
            collaborator_dict = response.json()
            collaborator_list = list(collaborator_dict.keys())
        
        # Create task dataframe
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

        # Ability to sort tasks 
        sort_by = st.selectbox("Sort Tasks", placeholder="Sort Tasks", options=df.columns.tolist(), index=0, label_visibility="collapsed")
        sort_order = st.radio("Task order", options=["Ascending", "Descending"], index=0)
        ascending = True if sort_order == "Ascending" else False
        df_sorted = df.sort_values(by=sort_by, ascending=ascending)
        df_sorted_reset = df_sorted.reset_index(drop=True)

        # Data editor for tasks 
        edited_df = st.data_editor(df_sorted_reset, num_rows="dynamic", column_config=column_config, use_container_width=True)

        # Button to update task data 
        if st.button("Save"):
            if edited_df is not None and not df_sorted_reset.equals(edited_df):
                if edited_df.isnull().values.any() or (edited_df == "").values.any():
                    st.error("All fields must be filled before updating")
                else:
                    edited_df["deadline"] = edited_df["deadline"].dt.strftime('%Y-%m-%d')
                    payload = {
                        "updated_tasks": edited_df.to_dict(orient="records"),
                        "project_name": st.session_state.project_name
                    }
                    
                    # Sends updates to the backend 
                    update_response = requests.post(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/task_updates", json=payload)
                    if update_response.status_code == 200:
                        st.rerun()
                        st.success("Data update saved successfully")
                    else:
                        st.error(f"Failed to save data. Status code: {update_response.status_code}")
            else:
                st.warning("No changes were made to the tasks")
    
        # Display categories  
        i = 1
        for category in filtered_category_list:
            st.sidebar.write(f"{i}. {category}")
            i = i + 1

        # Ability to remove categories 
        with st.sidebar.form("Category", clear_on_submit=True, border=False):
            with st.expander("Remove a Category"):
                selected_category = st.selectbox(f"Remove Category", filtered_category_list, index=None, placeholder="Category to Remove", label_visibility="collapsed")
                if st.form_submit_button("Remove"):
                    if selected_category != 'Select a category':
                        response = requests.post(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/remove_category", params={"project_name": st.session_state.project_name, "category": selected_category})
                        if response.status_code == 200:
                            st.rerun()
                            st.success(f"Category has been removed.")
                        else:
                            st.error("Error occurred while removing category.")
                    else:
                        st.error("Please select a category.")
    elif role == "Guest" or len(task_list) == 0:
        st.subheader("\n\nThere are no tasks to display.")
        
    
    
# Function to display team settings
def display_team_settings():

    col1, col2 = st.columns([4, 2])
    with col1:
        st.title(st.session_state.project_name + " Team Settings")
    
    # Logout button 
    if st.sidebar.button("Logout", key= 'Logout'):
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")
    # Return button to go back to project view 
    if st.sidebar.button("Back", key= 'Back'):
        del st.session_state["team_settings"]
        st.rerun()

    # Display team member list
    with st.sidebar:
        st.subheader("Team Members")
        response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/collaborators", params={"project_name": st.session_state.project_name})
        if response.status_code == 200:
            collaborator_dict = response.json()
            for collaborator, role in collaborator_dict.items():
                st.write(f"{collaborator} : {role}")
    
    # Collaborator management (OWNER ONLY)
    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/role", params={"project_name": st.session_state.project_name})
    if response.status_code == 200:
        role = response.json()

    if role == 'Owner':
        st.subheader("Add Collaborator")
        with st.form("Add", clear_on_submit=True, border=False):

            # Add Collaborators 
            col1, col2, col3 = st.columns(3)
            
            with col1:
                username_entry = st.text_input(label="Username", placeholder="Username", label_visibility="collapsed")

            with col2:
                user_role = st.selectbox('Role:', ('Select a role', 'Owner', 'Member', 'Guest'), label_visibility="collapsed")
            
            with col3:
                # Add button to add a new collaborator 
                if st.form_submit_button("Add"):
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

        # Update collaborator roles 
        st.subheader("Update Collaborator Role")
        with st.form("Update", clear_on_submit=True, border=False):
            col1, col2, col3 = st.columns(3)

            with col1:
                # Fetch collaborators 
                response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/collaborators", params={"project_name": st.session_state.project_name})
                if response.status_code == 200:
                    collaborator_dict = response.json()
                    collaborator_list = list(collaborator_dict.keys())
                    collaborator_list.remove(st.session_state.username)
                    collaborator = st.selectbox(f"Collaborator", ["Select a collaborator"] + collaborator_list, label_visibility="collapsed")

            with col2:
                # Role choices 
                new_role = st.selectbox('Role', ('Select a role', 'Owner', 'Member', 'Guest'), label_visibility="collapsed")

            with col3:
                # Update button to update the user's role 
                if st.form_submit_button(f'Update'):
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
                collaborator = st.selectbox(f"Collaborator to remove", ["Select a collaborator"] + collaborator_list, label_visibility="collapsed")
        
        with col2:
            # Button to remove a collaborator 
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


# Function to display the home page to choose between login or signup
def display_home():

    # Adjusting the 'Welcome to HoneyDue' to the center of the page. 
    display_company_logo()
    
    # Centered the buttons to the screen
    col1, col2, col3 = st.columns([.60,.50,1])
    
    with col2:
        # Login button 
        if st.button("Login", key= 'Login'):
            st.session_state.page = "login"
            st.rerun()

    with col3:
        # Sign up button 
        if st.button("Sign Up", key= 'SignUp'):
            st.session_state.page = "signup"
            st.rerun()

# Function to display the logo 
def display_company_logo():
    
    # Each screen will have the HoneyDue sign on the top
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
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("https://i.pinimg.com/originals/fe/be/ca/febeca2f63bd56c127069bac2fff9323.jpg",width=200) 
    st.markdown('<div class="header-title">HoneyDue</div>', unsafe_allow_html=True)

# Main application
def main():
    # Initialize session state variables 
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

# Application entry point 
if __name__ == "__main__":
    main()
