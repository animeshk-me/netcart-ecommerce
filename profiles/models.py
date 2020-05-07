from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50,default='firstname', blank=False)
    lastname  = models.CharField(max_length=50,default='lastname')
    address1  = models.CharField(max_length=200,default='add1')
    address2  = models.CharField(max_length=200,default='add2')
    phone     = models.IntegerField(default=0, blank=False)
    


    def __str__(self):
        return f'{self.user.username} Profile'