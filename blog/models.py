from django.db import models
from django.urls import reverse


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:article_list', args=[str(self.name)])
    

    class Meta:
        ordering = ['name'] 
        verbose_name = 'Article Category'
        verbose_name_plural = 'Article Categories'
    

class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ArticleCategory,
                                   on_delete=models.SET_NULL,
                                   null=True)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[str(self.pk)])
    

    class Meta:
        ordering = ['-created_on'] 
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
    