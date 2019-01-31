# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy sample data directory
COPY ./data /app/data

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ARG default_gunicorn_workers=4
ENV GUNICORN_WORKERS=$default_gunicorn_workers

# Run app.py when the container launches using gunicorn
CMD gunicorn -w $GUNICORN_WORKERS -b 0.0.0.0:80 transform:app 