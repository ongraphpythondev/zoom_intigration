from django.db import models

# Create your models here.

class ZoomAuth(models.Model):
    code = models.CharField(max_length=50)
    auth_token = models.CharField(max_length=100,null=True)
    update_time = models.DateTimeField(auto_now=True)