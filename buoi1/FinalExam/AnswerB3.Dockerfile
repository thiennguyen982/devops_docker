# Use this empty Dockerfile to build your assignment

# This dir contains Python app, you need to get it running in a container
# No modifications to the app should be necessary, only edit this Dockerfile

# Instructions from the app developer
# - you should use the 'ubuntu' official image
# - then it should install the Python pip package to the ubuntu linux distribution: 	
		# 'apt-get update -y'
		# 'apt-get install -y python-pip python-dev build-essential'
	# optimize it !
# - then it should create directory /usr/src/app/ for app files with 'mkdir -p /usr/src/app/'
# - then it needs to copy requirements.txt and app.py to /usr/src/app/
# - then it needs to run 'pip install --no-cache-dir -r /usr/src/app/requirements.txt' to install dependencies from that file
# - this app listens on port 5000, but the container should launch on port 80
  #  so it will respond to http://localhost:80 on your computer
# - then it needs to start container with command 'python /usr/src/app/app.py'
# - build this dockerfile with another optimize images and find a smallest

# FROM python:3-onbuild

# # RUN apt-get update -y && \
# # 	apt-get install -y python-pip python-dev build-essential

# RUN mkdir -p /usr/src/app/

# WORKDIR /usr/src/app

# COPY . .

# RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 80

# CMD [ "python", "./app.py" ]

# Use a lightweight base image like Alpine Linux
FROM ubuntu:18.04

# Set the working directory
WORKDIR /usr/src/app

# Install necessary system dependencies and Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python-dev \
    build-essential \
	  python-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80
EXPOSE 5000

# Command to start the application
CMD ["python", "./app.py"]

