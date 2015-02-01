#! /bin/sh
# /etc/init.d/car

export PROGRAM_NAME="car"
export FULL_PATH="/root/rpi-car/car.js"
export FILE_NAME="robot.js"
export NODE_PATH="/usr/bin/env node"
export NODE_ENV="daemon"

# Some things that run always
mkdir -p /var/log/$PROGRAM_NAME

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    export HOME="/root"
    echo "Starting car"
    echo $$ > /var/run/$PROGRAM_NAME.pid
    cd $FULL_PATH
    $NODE_PATH $FULL_PATH/$FILE_NAME
    ;;
  stop)
    echo "Stopping car"
    killall pi-blaster
    killall robot.js
    rm /var/run/$PROGRAM_NAME.pid
    ;;
  *)
    echo "Usage: /etc/init.d/car {start|stop}"
    exit 1
    ;;
esac

exit 0
