source myvenv/bin/activate

mysql -uroot -e 'revoke all privileges, grant option from project_ask_user@localhost'
mysql -uroot -e 'drop user project_ask_user@localhost'
mysql -uroot -e 'drop database project_ask'

mysql -uroot -e 'create database project_ask'
mysql -uroot -e 'create user project_ask_user@localhost identified with mysql_native_password by "Project_Ask1!"'
mysql -uroot -e 'grant all privileges on project_ask.* to project_ask_user@localhost'

python ask/manage.py migrate
