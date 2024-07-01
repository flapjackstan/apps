# Use an official Python runtime as a parent image
FROM python:3.12-bookworm

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Default command to start a bash shell
CMD ["bash"]
