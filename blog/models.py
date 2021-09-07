from django.db import models
from django.utils import timezone


# One to Many Relationship
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Special Method
    def __str__(self):
        return self.title
    
    

