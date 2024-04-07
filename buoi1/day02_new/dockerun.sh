name='hello-world'

docker run --name $name hello-world

echo; docker image ls | grep -E 'hello-world|IMAGE'

echo; docker ps -a

echo $name > ./o_dockerun.txt
