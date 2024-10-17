FROM python:3.9-slim

# Set working directory within docker container
WORKDIR /app

# Copy the requirements.txt for the backend into the container
COPY requirements.txt .

#  Pip install the requirements inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Copy main into the container inside of the current working directory (/app)
COPY main.py .

# Upon docker container spin up, instantiate the API hosted on 0.0.0.0:8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
