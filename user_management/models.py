from django.db import models
from django.urls import reverse


class Profile(models.Model):
    display_name = models.CharField(max_length=63)
    description = models.EmailField()

    def __str__(self):
        return self.name
