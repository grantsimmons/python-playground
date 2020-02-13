for ((i=0;i<3;i++))
do
    echo $1
    echo "Tracing $1, round $i"
    inetutils-traceroute --resolve-hostnames -M icmp $1 >> tracert_output.txt
done
