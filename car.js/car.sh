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
    cd $FULL_PATH
    forever start --command node --sourceDir $FULL_PATH --spinSleepTime=10000 --minUptime=1000 $FILE_NAME >> /var/log/$PROGRAM_NAME/info.log 2>&1
    ;;
  stop)
    echo "Stopping car"
    cd $FULL_PATH
    forever stop --command node --sourceDir $FULL_PATH $FILE_NAME >> /var/log/$PROGRAM_NAME/info.log 2>&1
    ;;
  *)
    echo "Usage: /etc/init.d/car {start|stop}"
    exit 1
    ;;
esac

exit 0
