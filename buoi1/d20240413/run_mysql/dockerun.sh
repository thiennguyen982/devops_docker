docker run \
    -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
    --name mysql_c \
    -p 3306:3306 \
    -d \
    mysql