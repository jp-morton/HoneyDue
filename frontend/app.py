import streamlit as st
import streamlit.components.v1 as components
from streamlit_calendar import calendar
import pandas as pd
import requests
import pathlib
from datetime import datetime

import streamlit as st
st.set_page_config(layout="wide")


API_URL = "http://backend:8000"

# Function to load CSS from folder
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("styles.css")
load_css(css_path)

st.logo("https://i.pinimg.com/originals/fe/be/ca/febeca2f63bd56c127069bac2fff9323.jpg", size="large")
# Helper function to handle user login
def login(username, password):
    response = requests.post(f"{API_URL}/login", params={"username": username, "password": password})
    return response.ok

# Helper function to handle user signup
def signup(username, password, verify_password):
    response = requests.post(f"{API_URL}/signup", params={"username": username, "password": password, "verify password": verify_password})
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

    display_company_logo()

    st.subheader("Login")
    with st.form("Login", clear_on_submit=True, border=False):
        username = st.text_input("Username", placeholder="Username", label_visibility="collapsed", key= 'goldInput1')
        password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed", key= 'goldInput2')

        if st.form_submit_button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
                st.success("Logged in successfully!")
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
        username = st.text_input("Create Username", placeholder= "New User", label_visibility="collapsed")
        password = st.text_input("Create Password", type="password", placeholder="Create Password", label_visibility="collapsed")
        verify_password = st.text_input("Confirm Password", type="password", placeholder="Confirm Password", label_visibility="collapsed")

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
   
    # Add "Back" button to return to previous page
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
            project_name = st.text_input("Enter a new project name", placeholder="New Project", label_visibility="collapsed")
            if st.form_submit_button("Create Project"):
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
                if st.button(f"{i}. {project}", key= f"Projects{i}"):
                    st.session_state.project_name = project
                    st.rerun()
                i = i + 1


def display_calendar():
    # Initialize state to avoid UnboundLocalError
    state = {}

    # Fetch tasks from the backend
    response = requests.get(
        f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/task",
        params={"project_name": st.session_state.project_name},
    )

    if response.status_code == 200:
        tasks = response.json()
        events = []


        priority_color_map  = {
            1: "#FF0000",  # Red for priority 1 (highest)
            2: "#FFFF00",  # Yellow for priority 2
            3: "#01FF23",  # Yellow for priority 3
            4: "#3301FF",  # Blue for priority 4
            5: "#F601FF",  # Green for priority 5 (lowest)
        }


        for task in tasks:
            if not task.get("deadline"):
                st.error(f"Task '{task['name']}' is missing a deadline.")
                return

            # Convert deadline to ISO 8601 format if not already
            try:
                start_date = datetime.strptime(task["deadline"], "%Y-%m-%d").isoformat()
            except ValueError:
                st.error(f"Task '{task['name']}' has an invalid deadline format.")
                return

            # Fetch the priority of the task and assign the corresponding color
            priority = int(task.get("priority", 5))  # Default to priority 5 if not specified
            color = priority_color_map.get(priority, "#3D9DF3")  # Default to blue if priority is invalid

            event = {
                "title": task["name"],
                "start": start_date,
                "end": start_date,
                "color": color,
            }
            events.append(event)
    else:
        st.error("Could not fetch tasks.")
        return

    # Set up calendar options
    calendar_options = {
        "initialView": "dayGridMonth",
        "editable": True,
        "navLinks": True,
        "displayEventTime": False,  # Disables time display
        "selectable": True,
    }

    # Render the calendar
    try:
        state = calendar(events=events, options=calendar_options, key="tasks_calendar")
    except Exception as e:
        st.error(f"Calendar rendering failed: {e}")

    # Ensure state is defined before accessing it
    if state:
        # if state.get("eventClick"):
        #     st.write("Selected Event Details:", state["eventClick"])

        if state.get("eventsSet"):
            st.session_state["events"] = state["eventsSet"]

        # Debugging output for state
        # st.write("Calendar State:", state)

# def display_calendar():
#     # Fetch tasks from the backend
#     response = requests.get(
#         f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/task",
#         params={"project_name": st.session_state.project_name},
#     )

#     if response.status_code == 200:
#         tasks = response.json()
#         # Format tasks for the calendar
#         events = []
#         for task in tasks:

#             # color_map = {"High": "#FF6C6C", "Medium": "#FFBD45", "Low": "#3DD56D"}
#             # event = {
#             #     "title": task["name"],
#             #     "start": task["deadline"],
#             #     "end": task["deadline"],
#             #     "color": color_map.get(task["priority"], "#3D9DF3"),
#             # }

#             task["deadline"] = datetime.strptime(task["deadline"], "%Y-%m-%d").isoformat()

#             event = {
#                 "title": task["name"],
#                 "start": task["deadline"],
#                 "end": task["deadline"],   # Use end dates if available
#                 "color": "#3D9DF3",        # Optional, set based on task priority/status
#             }
#             events.append(event)
#     else:
#         st.error("Could not fetch tasks.")
#         return
    

#     # mode = st.selectbox(
#     # "Calendar Mode:",
#     # ["daygrid", "timegrid", "list", "timeline"],
#     # )

#     # Set up calendar options
#     calendar_options = {
#         "initialView": "daygrid",
#         "editable": "true",
#         "navLinks": "true",
#         "selectable": "true",
#     }

#     # calendar_options["initialView"] = mode

#     # Render the calendar
#     # state = calendar(events=events, options=calendar_options, key="tasks_calendar")

#     # Handle selected event (if any)
#     if state.get("eventClick"):
#         st.write("Selected Event Details:", state["eventClick"])

#     # Handle newly added or updated events
#     if state.get("eventsSet"):
#         st.session_state["events"] = state["eventsSet"]

#     # Render the calendar
#     try:
#         state = calendar(events=events, options=calendar_options, key="tasks_calendar")
#         st.write(state)
#     except Exception as e:
#         st.error(f"Calendar rendering failed: {e}")


#Function for displaying color coding tasks
def display_priority_color_code():
    # Define colors for different priorities
    priority_color_map = {
        1: "#FF0000",  # Red for priority 1 (highest)
        2: "#FFFF00",  # Yellow for priority 2
        3: "#01FF23",  # Green for priority 3
        4: "#3301FF",  # Blue for priority 4
        5: "#F601FF",  # Purple for priority 5 (lowest)
    }

    st.sidebar.subheader("Priority Color Code")
    for priority, color in priority_color_map.items():
        st.sidebar.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="width: 15px; height: 15px; background-color: {color}; border-radius: 3px; margin-right: 8px;"></div>
                <span>Priority {priority}</span>
            </div>
            """,
            unsafe_allow_html=True
        )


def display_tasks():
    st.subheader(f"{st.session_state.project_name} Homepage")

    if st.sidebar.button("Logout", key= 'Logout'):
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")

    if st.sidebar.button("Back", key= 'Back'):
        del st.session_state.project_name
        st.rerun()

    if st.sidebar.button("Team Settings", key= 'TeamSet'):
            st.session_state["team_settings"] = True
            st.rerun()

    if st.sidebar.button("Manage Tasks", key= 'TaskMan'):
        st.session_state["task_list"] = True
        st.rerun()

    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/role", params={"project_name": st.session_state.project_name})
    if response.status_code == 200:
        role = response.json()

    st.sidebar.markdown("---")
    
    display_priority_color_code()

    # CALENDAR PLACEHOLDER
    display_calendar()

# Function to display tasks and add new tasks

def display_task_list():

    # Log out button
    if st.sidebar.button("Logout", key= 'Logout'):
        st.session_state.clear()
        st.rerun()
    
    st.sidebar.markdown("---")
        
    # Back button
    if st.sidebar.button("Back", key= 'Back'):
        del st.session_state["task_list"]
        st.rerun()
    
    col1, col2 = st.columns(2)

    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/role", params={"project_name": st.session_state.project_name})
    if response.status_code == 200:
        role = response.json()

    # COL2 OF TASKS PAGE
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
                    #status = "TODO"

                    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/category", params={"project_name": st.session_state.project_name})
                    if response.status_code == 200:
                        category_list = response.json()
                        category = st.selectbox(f"Category", category_list, index=None, placeholder="Category", label_visibility="collapsed")

                    
                    status = st.selectbox("Task Status", options=["TODO", "DOING", "DONE"], index=None, placeholder="Task Status", label_visibility= "collapsed")

                    response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/collaborators", params={"project_name": st.session_state.project_name})
                    if response.status_code == 200:
                        collaborator_dict = response.json()
                        collaborator_list = list(collaborator_dict.keys())
                        collaborator_list.remove(st.session_state.username)
                        assignee = st.selectbox(f"Assignee", ["Assign to me"] + collaborator_list, index=None, placeholder="Assign To" ,label_visibility="collapsed")

                
                    if st.form_submit_button("Add Task"):
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

   
        if role != "Guest":
            
            with st.sidebar.form("Add", clear_on_submit=True, border=False):
                
                    category_entry = st.text_input("Category: ", placeholder="Category", label_visibility="collapsed")

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
        
        # Get user role
        response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/role", params={"project_name": st.session_state.project_name})
        if response.status_code == 200:
            role = response.json()

        # Get task list
        response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/task", params={"project_name": st.session_state.project_name})
        if response.status_code == 200:
            task_list = response.json()

    if len(task_list) != 0 and role != "Guest":        
        # Get category list
        response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/category", params={"project_name": st.session_state.project_name})
        if response.status_code == 200:
            category_list = response.json()
            filtered_category_list = category_list.copy()
            filtered_category_list.remove("None")

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

        sort_by = st.selectbox("Sort Tasks", placeholder="Sort Tasks", options=df.columns.tolist(), index=0, label_visibility="collapsed")
        sort_order = st.radio("Task order", options=["Ascending", "Descending"], index=0)
        ascending = True if sort_order == "Ascending" else False
        df_sorted = df.sort_values(by=sort_by, ascending=ascending)
        df_sorted_reset = df_sorted.reset_index(drop=True)

        edited_df = st.data_editor(df_sorted_reset, num_rows="dynamic", column_config=column_config, use_container_width=True)

        # Update button
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
                    
                    update_response = requests.post(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/task_updates", json=payload)
                    if update_response.status_code == 200:
                        st.rerun()
                        st.success("Data update saved successfully")
                    else:
                        st.error(f"Failed to save data. Status code: {update_response.status_code}")
            else:
                st.warning("No changes were made to the tasks")
    
        i = 1
        for category in filtered_category_list:
            st.sidebar.write(f"{i}. {category}")
            i = i + 1

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
    
    if st.sidebar.button("Logout", key= 'Logout'):
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")
    # Return button
    if st.sidebar.button("Back", key= 'Back'):
        del st.session_state["team_settings"]
        st.rerun()

    with st.sidebar:
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
        with st.form("Add", clear_on_submit=True, border=False):

            # Add Collaborators 
            col1, col2, col3 = st.columns(3)
            
            with col1:
                username_entry = st.text_input(label="Username", placeholder="Username", label_visibility="collapsed")

            with col2:
                user_role = st.selectbox('Role:', ('Select a role', 'Owner', 'Member', 'Guest'), label_visibility="collapsed")
            
            with col3:
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

        # Update Role
        st.subheader("Update Collaborator Role")
        with st.form("Update", clear_on_submit=True, border=False):
            col1, col2, col3 = st.columns(3)

            with col1:
                response = requests.get(f"{API_URL}/{st.session_state.username}/{st.session_state.project_name}/collaborators", params={"project_name": st.session_state.project_name})
                if response.status_code == 200:
                    collaborator_dict = response.json()
                    collaborator_list = list(collaborator_dict.keys())
                    collaborator_list.remove(st.session_state.username)
                    collaborator = st.selectbox(f"Collaborator", ["Select a collaborator"] + collaborator_list, label_visibility="collapsed")

            with col2:
                new_role = st.selectbox('Role', ('Select a role', 'Owner', 'Member', 'Guest'), label_visibility="collapsed")

            with col3:
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
    display_company_logo()
    
    #Centered the buttons to the screen
    col1, col2, col3 = st.columns([.60,.50,1])
    
    with col2:
        if st.button("Login", key= 'Login'):
            st.session_state.page = "login"
            st.rerun()

    with col3:
        if st.button("Sign Up", key= 'SignUp'):
            st.session_state.page = "signup"
            st.rerun()

def display_company_logo():
    
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
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("https://i.pinimg.com/originals/fe/be/ca/febeca2f63bd56c127069bac2fff9323.jpg",width=200) 
    st.markdown('<div class="header-title">HoneyDue</div>', unsafe_allow_html=True)

# Main application
def main():
    
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

if __name__ == "__main__":
    main()
