#! /bin/sh

set -e

sudo apt install python3-lgpio python3-rpi.gpio

echo "=> Installing fan controller...\n"
sudo cp ./fancontrol.py /usr/local/bin/
sudo chmod +x /usr/local/bin/fancontrol.py


echo "=> Starting fan controller...\n"
sudo cp ./fancontrol.sh /etc/init.d/
sudo chmod +x /etc/init.d/fancontrol.sh

sudo update-rc.d fancontrol.sh defaults
sudo /etc/init.d/fancontrol.sh start

echo "Fan controller installed."
