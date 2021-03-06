#!/bin/sh
echo 470 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio470/direction

echo 474 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio474/direction

echo 478 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio478/direction

echo 479 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio479/direction

while true; do 
	# red
	echo 1 > /sys/class/gpio/gpio470/value
	sleep 1
	echo 0 > /sys/class/gpio/gpio470/value

	# green
        echo 1 > /sys/class/gpio/gpio474/value
        sleep 1
        echo 0 > /sys/class/gpio/gpio474/value

	# yellow
        echo 1 > /sys/class/gpio/gpio478/value
        sleep 1
        echo 0 > /sys/class/gpio/gpio478/value

	# blue
        echo 1 > /sys/class/gpio/gpio479/value
        sleep 1
        echo 0 > /sys/class/gpio/gpio479/value
done
