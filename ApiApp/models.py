from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class Client(AbstractUser):
    img = models.ImageField(upload_to='clients/',null=True,blank=True)
    date = models.DateTimeField(null=True,blank=True)

class Task(models.Model):
    title = models.CharField(max_length=255)
    is_check = models.BooleanField(default=False)
    user = models.ForeignKey(Client,on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.title
