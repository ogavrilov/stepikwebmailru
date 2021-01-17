#prepare os, python
sudo apt-get update
sudo apt-get install -y python3.5
sudo apt-get install -y python3.5-dev
# prepare virtual environment
virtualenv -p python3.5 myvenv
source myvenv/bin/activate
# prepare libs
pip3 install --upgrade pip
pip3 install --upgrade django==2.1
pip3 install --upgrade gunicorn
# prepare and start nginx
sudo mkdir /home/box/web/log
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/nginx.conf
sudo /etc/init.d/nginx restart
#prepare and start gunicorn
sudo kill -KILL $(pgrep -f gunicorn|tr '\n' ' ')
gunicorn --bind 0.0.0.0:8080 --pythonpath /home/box/web hello:app &
gunicorn --bind 0.0.0.0:8000 --pythonpath /home/box/web/ask ask.wsgi:application &
