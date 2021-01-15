sudo mkdir /home/box/web/log
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/nginx.conf
sudo ln -sf /home/box/web/etc/gunicorn.conf /etc/gunicorn.d/test
sudo /etc/init.d/nginx restart
sudo gunicorn --bind 0.0.0.0:8080 hello:app
