from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# User model

class UserProfile(AbstractUser):
    first_name = models.CharField(max_length=150)
    password = models.CharField(max_length=8, null=True, blank=True)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email_address = models.EmailField("email address", unique=True)

    def __str__(self):
        return self.username


    

