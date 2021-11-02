from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Userdetails(models.Model):
    user1=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.TextField(max_length=200)
    dob=models.DateTimeField()
    # friends= models.ListField(User)

# class Chat(models.Model):
#     from_recipe
#     to_recp
#     timestamp
#     text
#     subject

