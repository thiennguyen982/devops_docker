SH=`cd $(dirname $BASH_SOURCE) && pwd`

cd $SH

docker-compose exec postgres_c bash -c 'echo POSTGRES_PASSWORD=$POSTGRES_PASSWORD'