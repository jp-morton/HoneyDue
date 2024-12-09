# Temporary README until i figure out how to actually use markdown
LAST UPDATE: 26 SEP 2024

Environment setup (for develoment only)
-----------------
Once you pull down the repo, you will need to set up your environment. Utilizing virtual environments helps
to keep installed dependecies installed in the proper locations without affecting your actual host system environment.

1. Change directory to HoneyDue/

2. Create the virtual environment in the top-most level of the HoneyDue project
    > python3 -m venv .venv

    You may have to install python3.10-venv in order to do this. If you get an error, install this.
    > sudo apt install python3.10-venv

3. Activate the virutal environment
    > source .venv/bin/activate

Your environment should now be properly configured. 


Running HoneyDue
--------------------------------------
As prerequisites for the following you will need to install the following:

docker              https://docs.docker.com/engine/install/ubuntu/
docker-compose      https://docs.docker.com/compose/install/linux/#install-using-the-repository

> Clone the repository
    git clone {repository url}

> Navigate to project repository
    HoneyDue/

> Launch the docker containers
    docker compose up

> Open a browser and navigate to the following...
    0.0.0.0:8501

> HoneyDue has been launched!