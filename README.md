### 服务器环境首次部署步骤：

步骤1.生成虚拟环境venv安装项目所需要的包; 步骤2.配置Nginx服务; 步骤3.开启uwsgi服务

#### 步骤1.生成虚拟环境venv安装项目所需要的包

Python版本3.9.7

```shell
git clone https://src.cloudminds.com/sevel.liu/nlpauto.git
cd nlpauto
pip install virtualenv
virtualenv --prefix=/opt/python397/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 步骤2.配置Nginx服务

修改`conf/nlpauto_nginx.conf`配置文件，将文件中的绝对路径替换成当前项目所在服务器的绝对路径。然后执行以下命令：

Note：此项目Nignx服务默认占用8088端口

```shell
cd nlpauto
sudo ln -s conf/nlpauto_nginx.conf /etc/nginx/conf.d/nlpauto_nginx.conf
systemctl restart nginx
```

#### 步骤3.开启uwsgi服务

先生成静态文件

```shell
source venv/bin/activate
pip install uwsgi
python manage.py collectstatic
```

修改`conf/env.py`文件，设置数据库等信息，执行命令生成数据库表：

```shell
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

修改`settings.py`文件，设置为`DEBUG=False`

修改`conf/uwsgi.ini`文件，将文件中的绝对路径替换成当前项目所在服务器的绝对路径。然后执行以下命令：

Note：此项目uwsgi服务默认占用8000端口

```shell
uwsgi --ini conf/uwsgi.ini
```

浏览器验证：

```shell
http://xxx.xxx.xxx.xxx:8088
```
### 服务器环境非首次部署步骤：

步骤1.执行shell脚本`start.sh`

```shell
git pull
bash start.sh
```

### 本地环境部署步骤：

步骤1.修改`conf/env.py`文件，设置数据库等信息，执行命令生成数据库表：

```shell
python manage.py makemigrations
python manage.py migrate
```

步骤2.修改`settings.py`文件，设置为`DEBUG=True`

步骤3.Pycharm工具启动

```
python manage.py runserver
```

浏览器验证：

```shell
http://127.0.0.1:8000
```