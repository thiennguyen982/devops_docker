# use this empty Dockerfile to build your assignment

# This dir contains a Node.js and Python app, you need to get it running in a container
# No modifications to the app should be necessary, only edit this Dockerfile

# Instructions from the app developer
# - you should use the 'ubuntu' official image
FROM ubuntu:18.04

# - then it should install packages dependencies: 	
		# 'apt-get -yqq update'
		# 'apt-get -yqq install python-pip python-dev curl gnupg'
		# 'apt-get install -yq nodejs npm'
	# optimize it !
RUN apt-get -yqq update && \
	apt-get -yqq install python-pip python-dev curl gnupg && \
	apt-get install -yq nodejs npm && \
	mkdir -p /opt/flask-app

# - then it should create directory /opt/flask-app for app files with 'mkdir -p /opt/flask-app'
WORKDIR /opt/flask-app

# - then it needs to copy /opt/flask-app from flask-app
COPY ./flask-app .

# - then it needs to run 'npm install' to install dependencies from that file
# - then it needs to run 'npm run build'
# - then it needs to run 'pip install -r requirements.txt' to install dependencies from that file
RUN npm install && \
	npm run build && \
	pip install --no-cache-dir -r requirements.txt && \
	apt-get clean autoclear && \
	rm -rf /var/lib/apt/lists/*

# - this app listens on port 5000, but the container should launch on port 80
EXPOSE 5000

  #  so it will respond to http://localhost:80 on your computer
# - then it needs to start container with command 'python ./app.py'
CMD [ "python", "./app.py" ]