docker container run -d \
    --network mybridge \
    --name drupal_c \
    --publish 8080:80 \
    drupal:latest

docker container run -d \
    --network mybridge \
    --name mariadb_c  \
    --env MARIADB_ROOT_PASSWORD=123qe \
    --publish 3306:80 \
    mariadb:latest
