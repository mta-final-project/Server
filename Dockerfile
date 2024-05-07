# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Set env variable to allow imports from src
ENV PYTHONPATH="$PYTHONPATH:/app/src/"


# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Start the application when the container starts
ENTRYPOINT ["python"]
CMD ["src/main.py"]