curl -s "localhost:88" | grep h1

c='run_nginx_custome_welcome_nginx_c_1'

docker exec $c bash -c 'echo; /usr/share/nginx/html/index.html'

docker exec $c bash -c 'echo; cp /usr/share/nginx/html/index.html /usr/share/nginx/html/index.html.origin'

docker exec $c bash -c 'echo; ls /usr/share/nginx/html/'

docker exec $c bash -c 'echo; echo "Welcome to lop docker nha!!" > /usr/share/nginx/html/index.html'