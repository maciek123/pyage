port=9000
for i in `cat machines` 
do 
	ssh -f jagular -L $port:$i:22 -N
	let "port=$port+1"
done
