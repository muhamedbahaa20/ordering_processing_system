from django.contrib.auth.models import AbstractUser
from django.db import models

class Customer(AbstractUser):
    # name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, null=True)
    # password = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    groups = None
    user_permissions = None

    def  __str__(self):
        return self.username