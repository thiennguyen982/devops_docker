#Tao card mang ca nhan mybridge
docker network create -d bridge mybridge

#Pull registry
docker run -d \
    -p 5000:5000 \
    --net mybridge \
    --restart always \
    --name registry \
    registry:2

#Pull registry_ui
docker run -d \
    -p 8080:80 \
    --net mybridge \
    -e DELETE_IMAGES=true \
    -e REGISTRY_URL=http://registry:5000 joxit/docker-registry-ui:static

#Pulling alpine
docker pull alpine:latest

#Create tagging
docker tag alpine 192.168.15.11:5000/alpine:v1

#Pushing image to the docker registry
docker push 192.168.15.11:5000/alpine:v1

#Issue => The push refers to repository [192.168.15.11:5000/alpine]
#Get "https://192.168.15.11:5000/v2/": 
#http: server gave HTTP response to HTTPS client
#Fixing:
# vi /etc/docker/daemon.json
# Inserting:
# {
#     "insecure-registries":["192.168.15.11:5000"]
# }