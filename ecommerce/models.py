from django.db import models

class Login_model(models.Model):
    email = models.EmailField(blank=False, null=False)
    name = models.CharField(max_length = 120, blank=False, null=False)
    password = models.CharField(max_length = 10, blank=False)

class Register_model:
    email = models.EmailField(blank=False, null=False)
    name = models.CharField(max_length = 120, blank=False, null=False)
    password = models.CharField(max_length = 10, blank=False)



