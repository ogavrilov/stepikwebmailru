#sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo mkdir /home/box/web/log
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/nginx.conf
sudo /etc/init.d/nginx restart
