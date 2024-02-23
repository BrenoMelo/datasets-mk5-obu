#!/bin/bash

COUNTER=0
while true
do
    rand_run=$(( $RANDOM % 26 + 5));
    rand_stop=$(( $RANDOM % 16 + 5))

	echo "Iperf application will be running for $rand_run seconds. Next run will be in $rand_stop seconds.";
    sudo iperf --client=192.168.234.1 -t $rand_run --tradeoff --interval=1 --format=m --tos=MK2_PRIO_4
        #timeout $rand_run sudo ./runtest_iperf_tx.sh

    if [ $((COUNTER)) -eq 199 ]; then
        exit 1
    fi

    sleep $rand_stop

    COUNTER=$(( COUNTER + 1 ))
done
