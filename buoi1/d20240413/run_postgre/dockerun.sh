docker run \
    -e POSTGRES_PASSWORD=p@ssw0rd \
    --name postgres_c1 \
    -p 54322:5432 \
    -d \
    postgres