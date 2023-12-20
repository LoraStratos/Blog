from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    image = models.ImageField(upload_to='user_image', blank=True, null=True)
    page = models.OneToOneField('Profile', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('Message', on_delete=models.CASCADE, null=True, blank=True)


class Profile(models.Model):
    date_birth = models.DateTimeField(verbose_name='Дата рождения', null=True, auto_now_add=True)
    status = models.CharField(max_length=1000, blank=True, default='Новый')
    about = models.TextField(max_length=1000, blank=True, default='Обо мне')


class Message(models.Model):
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, db_column='person')
    page = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(max_length=1000, blank=True, default='')
    image = models.ImageField(upload_to='comments_image', blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    destination = models.CharField(max_length=299, null=True, blank=True)
