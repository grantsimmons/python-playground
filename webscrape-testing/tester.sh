for ((i=0;i<300;i++))
do
    echo $1
    echo "Tracing $1, round $i"
    date "+%Y-%m-%d %H:%M:%S" >> trace_$1.txt
    inetutils-traceroute --resolve-hostnames -M icmp $1 >> trace_$1.txt
    echo "Tracing $2, round $i"
    date "+%Y-%m-%d %H:%M:%S" >> trace_$2.txt
    inetutils-traceroute --resolve-hostnames -M icmp $2 >> trace_$2.txt
    sleep(250)
done
