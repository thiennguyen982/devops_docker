#Build images
docker build -t "<name>:<version>" .

#Create tagging
docker tag "<image_id>" "<docker_hub_username>/<name:tag>"

#Pushing
docker push "<docker_hub_username>/<name:tag>"

#Running
docker run -d -p "<external_ports>:<internal_port>" "<docker_hub_username>/<name:tag>"
