from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from autoslug import AutoSlugField

# Create your models here.
class Userdetails(models.Model):
    user1=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.TextField(max_length=200)
    dob=models.DateTimeField(auto_now=True)
    # friends = models.ManyToManyField("Userdetails", blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField("Profile", blank=True)
    slug = AutoSlugField(populate_from='user')

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return "/authentication/{}".format(self.slug)

# class FriendRequest(models.Model):
#     to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
#     from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "From {}, to {}".format(self.from_user.username, self.to_user.username)

# class Chat(models.Model):
#     from_recipe
#     to_recp
#     timestamp
#     text
#     subject

