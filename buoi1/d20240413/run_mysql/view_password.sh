SH=`cd $(dirname $BASH_SOURCE) && pwd`

cd $SH

docker container logs mysql | grep 'ROOT PASSWORD' --color=always