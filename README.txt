# Temporary README until i figure out how to actually use markdown
LAST UPDATE: 26 SEP 2024

Environment setup
-----------------
Once you pull down the repo, you will need to set up your environment. Utilizing virtual environments helps
to keep installed dependecies installed in the proper locations without affecting your actual host system environment.

1. Change directory to HoneyDue/

2. Create the virtual environment in the top-most level of the HoneyDue project
    > python3 -m venv .venv

    You may have to install python3.10-venv in order to do this. If you get an error, install this.
    > sudo apt install python3.10-venv

3. Activate the virutal environment
    > source .venv/bin/Activate

Your virtual environment should now be properly configured. 


Running the current state of the tool
--------------------------------------
The current version of things in the repo is very bare bones and intended to serve as a framework on which to flesh
out the rest of the HoneyDue app. Currently, we are utilizing three docker containers;
one each for the frontend/backend/database

1. Open the terminal and run the following command from the HoneyDue/ directory
    > docker compose up

2. This will spin up the docker environment. You'll see a bunch of stuff dumped out to the terminal. This is normal.
    Once this is done and you see the three containers start, open a browser and navigate to the following IP address:
    > 0.0.0.0:8501

3. You should now be at the streamlit frontend. You will see a message from the backend. This showcases the frontend and backend
    containers communicating together. The database container is currently not utilized as there is no use for it in the current,
    barebones configuration of HoneyDue