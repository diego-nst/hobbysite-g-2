from django.db import models
from django.urls import reverse


class PostCategory(models.Model):
    name = models.CharField(max_length=255, null = True)
    description = models.TextField(null = True)

    def __str__(self):
        return '{}'.format(self.name)
    
    def get_absolute_url(self):
        return reverse('forum:post_category', args=[str(self.name)])


class Post(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        PostCategory, 
        on_delete=models.SET_NULL,
        null = True,
        related_name="post_category"
        )
    entry = models.TextField(null = True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('forum:post_detail', args=[str(self.pk)])
    

# Create your models here.