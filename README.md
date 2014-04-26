Installation
====
```
git clone git@github.com:arduino-inbox/rpi-car.git
cd rpi-car
vagrant up
```


Provision RPi
====
```
ssh <rpi>
if [ -z `which python2` ]; then sudo pacman -Sy --noconfirm python2; fi
exit
vi provisioning/hosts  # replace alarmpi.local with your rpi host/ip
ansible-playbook --sudo --inventory-file=provisioning/hosts provisioning/site.yml
```
