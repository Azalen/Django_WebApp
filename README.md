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