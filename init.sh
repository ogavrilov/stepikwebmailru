#prepare os, python
sudo apt-get update
sudo apt-get install -y python3.5
sudo apt-get install -y python3.5-dev
#
sudo apt-get install -y debconf-utils
export DEBIAN_FRONTEND=noninteractive
debconf-set-selections <<< 'mysql-apt-config mysql-apt-config/select-product select Ok'
sudo wget http://dev.mysql.com/get/mysql-apt-config_0.7.2-1_all.deb
sudo dpkg -i mysql-apt-config_0.7.2-1_all.deb
sudo apt-get update
sudo apt-get install -y mysql-server-5.7
sudo apt-get install --assume-yes mysql-server-5.7 mysqlclient
# prepare virtual environment
virtualenv -p python3.5 myvenv
source myvenv/bin/activate
# prepare libs
pip3 install --upgrade pip
pip3 install --upgrade django
pip3 install --upgrade gunicorn
pip3 install --upgrade mysqlclient
# prepare and start nginx
sudo mkdir /home/box/web/log
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/nginx.conf
sudo /etc/init.d/nginx restart
# prepare mysql server, database and user
sudo /etc/init.d/mysql start
#sudo service mysql restart
#mysql -uroot -e 'revoke all privileges, grant option from project_ask_user@localhost'
#mysql -uroot -e 'drop user project_ask_user@localhost'
#mysql -uroot -e 'drop database project_ask'

mysql -uroot -e 'create database project_ask'
mysql -uroot -e 'create user project_ask_user@localhost identified by "Project_Ask1!"'
mysql -uroot -e 'grant all privileges on project_ask.* to project_ask_user@localhost'

python ask/manage.py makemigrations
python ask/manage.py migrate
#prepare and start gunicorn
sudo kill -KILL $(pgrep -f gunicorn|tr '\n' ' ')
gunicorn --bind 0.0.0.0:8080 --pythonpath /home/box/web hello:app &
gunicorn --bind 0.0.0.0:8000 --pythonpath /home/box/web/ask ask.wsgi:application &
