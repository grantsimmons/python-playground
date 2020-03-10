for ((i=0;i<86400;i++))
do
    for var in "$@"
    do
        echo $var
        echo "Digging $var, round $i"
        date "+%Y-%m-%d %H:%M:%S" >> dig_$var.txt
        dig +norecurse $var >> dig_$var.txt
    done
    echo "Sleeping"
    sleep 1
done
