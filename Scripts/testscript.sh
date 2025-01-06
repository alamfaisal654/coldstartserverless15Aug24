echo "$1"
for i in {1..10}
do  
	echo "$i";
	bash -c "(curl -H 'Host: hello-world.example' http://localhost:22567) &";
done

