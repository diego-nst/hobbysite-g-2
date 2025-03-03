from datetime import datetime

from django.db import models
from django.urls import reverse

# Create your models here.


# Create your models here.

class ArticleCategory(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.pk])


class Article(models.Model):
    title = models.CharField(max_length=100)
    entry = models.TextField()
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="article"
    )
    
    #WIP
    @property
    def created_on(self):
        return datetime.now()

    #WIP
    @property
    def updated_on(self):
        return datetime.now()

    