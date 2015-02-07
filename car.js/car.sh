#! /bin/sh
# /etc/init.d/car

export PROGRAM_NAME="car"
export FULL_PATH="/root/rpi-car/car.js"
export FILE_NAME="robot.js"
export NODE_ENV="daemon"
export HOME="/root"

# Some things that run always
mkdir -p /var/log/$PROGRAM_NAME

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting car"
    forever start --spinSleepTime=30000 --minUptime=30000 $FULL_PATH/$FILE_NAME
    ;;
  stop)
    echo "Stopping car"
    forever stop $FULL_PATH/$FILE_NAME
    ;;
  *)
    echo "Usage: /etc/init.d/car {start|stop}"
    exit 1
    ;;
esac

exit 0
