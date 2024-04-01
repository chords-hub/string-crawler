# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Create a non-root user and give it ownership of the /app directory
RUN useradd -u 10014 -m myuser && mkdir /app && chown -R myuser /app

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Switch to the non-root user
USER 10014

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["python", "main.py"]