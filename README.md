# Django_WebApp

## Install VSCode

## Install Python3, pip & virtualenv

sudo apt-get install python3
pip install virtualenv

```
virtualenv django_project
source django_project/bin/activate
```

## 0.2 Django

```
django-admin manage.py startproject blogsite
python manage.py runserver
python manage.py startapp blog
```

## 0.3 Database Queries

// Arbeiten auf der db.sqlite3 d.h. es wird direkt in DB gefüllt
python manage.py shell

// Importieren der Klassen / DB-Einträge
>>> from blog.models import Post
>>> from django.contrib.auth.models import User

// Queries für die importierten Modelle
>>> User.objects.all()
                .filter(username='admin')
                .first()
                .get(id=1)

        => Dieses Objekt kann einer Variable (user) zugewiesen werden!

>>> user = User.objects.first()
    ACHTUNG: die hier erstellten Variablen sind lokal until .save() schreibt sie in die DB
.
// create Post-Objekt
>>> post_1 = Post(title='Blog 1', content='First Content', author=user)
// save it to DB
>>> post_1.save()

// to have nice output for a post we create special `__str__` method in blog/models.py (double underscore method)

// to get all Posts written by specific User via NameOfRelatedModel_set
>>> user.post_set.all()

// to create Post from specific user directly to DB
>>> user.post_set.create(title='Blog 3', content='Third Content')

// to exit
>>> exit()

## 0.4 Environment Variables on Linux

Never Hardcode Login-Information into your .py files but use Operating System Environmental Variables
-> https://mkyong.com/linux/how-to-set-environment-variable-in-ubuntu/

/etc/profile.d/myenv.sh
    export EMAIL_USER = ""             # LogIn Mail Adress for GMAIL
    export EMAIL_PASS = ""             # GMAIL Password

-> Restart, test with ~/source $EMAIL_USER afterwards

## 0.5 Deployment using Linode
ACHTUNG: Funktionierte nur mit Ubuntu18, bei neueren Versionen war irgendwas mit den Rechten komisch

-> SSH into machine and install some updates
    `ssh root@172.105.77.247`
    `apt-get update && apt-get upgrade`

-> Change hostname and set in hosts file
    `hostnamectl set-hostname django-server`
    `sudo nano /etc/hosts`
    -> 172.105.77.247   django-server

-> Add limited user and give sudo privilige
    `adduser azalen`
    `adduser azalen sudo`
    `ssh azalen@172.105.77.247`

-> Set up SSH Key based Auth (Best Practice)
    -> Generate Key-Pair and put public key on the server for automatic authentification
    on Server
    `mkdir -p ~/.ssh`
    on local Client
    `ssh-keygen -b 4096`
    `scp /home/azalen/.ssh/id_rsa.pub azalen@172.105.77.247:~/.ssh/authorized_keys`

    `sudo chmod 700 ~/.ssh/`
    `sudo chmod 600 ~/.ssh/*`

    7 = Read Write Execute
    6 = Read Write

    azalen@django-server:~$ 
    azalen@ubuntu:~$

-> Disallow Password Auth & Setup Firewall (Check Video)
    azalen@django-server:~$ sudo nano /etc/ssh/sshd_config -> Set Password Settings to No
    azalen@django-server:~$ sudo systemctl restart sshd
    azalen@django-server:~$ sudo apt-get install ufw

    azalen@django-server:~$ sudo ufw default allow outgoing 
    azalen@django-server:~$ sudo ufw default deny incoming
    azalen@django-server:~$ sudo ufw allow ssh
    azalen@django-server:~$ sudo ufw allow 8000

    azalen@django-server:~$ sudo ufw enable 

-> Create Requirements.txt from virtualenv (Python)
    azalen@ubuntu:~$ source ~/Environments/django_env/bin/activate  
    (django_env) azalen@ubuntu:~$ pip freeze > requirements.txt

-> Copy WebApp onto Server
    azalen@ubuntu:~$ scp -r Django_WebApp/ azalen@172.105.77.247:~/

-> Create VirtualEnv on Server
    azalen@django-server:~$ sudo apt-get install python3-pip
    azalen@django-server:~$ sudo apt-get install python3-venv

    azalen@django-server:~$ python3 -m venv Django_WebApp/venv
    azalen@django-server:~/Django_WebApp$ source venv/bin/activate
    (venv) azalen@django-server:~/Django_WebApp$ pip install -r requirements.txt 

-> Use Apache2 and modWSGI as Webserver instead of Django
    azalen@django-server:~$ sudo apt-get install apache2
    azalen@django-server:~$ sudo apt-get install libapache2-mod-wsgi-py3

    (venv) azalen@django-server:~/Django_WebApp$ cd /etc/apache2/sites-available/
    (venv) azalen@django-server:/etc/apache2/sites-available$ sudo cp 000-default.conf django_webapp.conf
    (venv) azalen@django-server:/etc/apache2/sites-available$ sudo nano django_webapp.conf 

        ```
        Alias /static /home/azalen/Django_WebApp/static
        <Directory /home/azalen/Django_WebApp/static>
                Require all granted
        </Directory>

        Alias /media /home/azalen/Django_WebApp/media
        <Directory /home/azalen/Django_WebApp/media>
                Require all granted
        </Directory>

        <Directory /home/azalen/Django_WebApp/Django_WebApp>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>

        WSGIScriptAlias / /home/azalen/Django_WebApp/Django_WebApp/wsgi.py
        WSGIDaemonProcess django_app python-path=/home/azalen/Django_WebApp python-home=/home/azalen/Django_WebApp/venv
        WSGIProcessGroup django_app
        ```

    (venv) azalen@django-server:~$ sudo a2ensite django_webapp
    (venv) azalen@django-server:~$ sudo a2dissite 000-default.conf 

    // Permissions: Apache Gruppe ist www-data und braucht vollen Zugriff auf die DB und muss auch in der Lage sein im 
    //              media Ordner zu schreiben, falls Nutzer Profilbilder hochladen

    (venv) azalen@django-server:~$ sudo chown :www-data Django_WebApp/db.sqlite3 
    (venv) azalen@django-server:~$ sudo chmod 664 Django_WebApp/db.sqlite3 
    (venv) azalen@django-server:~$ sudo chown :www-data Django_WebApp/
    (venv) azalen@django-server:~$ sudo chown -R :www-data Django_WebApp/media/
    (venv) azalen@django-server:~$ sudo chmod -R 775 Django_WebApp/media/

-> Move sensitive Information to Config File
    
