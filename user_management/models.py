from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    '''
    Profile model, foreign key to user

    has display_name, email, and slug
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=63)
    email = models.EmailField()
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return self.display_name
