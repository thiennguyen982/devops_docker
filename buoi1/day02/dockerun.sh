SH=`cd $(dirname $BASH_SOURCE) && pwd`
docker run \
	-p 88:80 -d \
	-v "$SH/html":/usr/share/nginx/html \
	nginx
