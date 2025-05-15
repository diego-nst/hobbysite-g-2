from django.db import models
from django.urls import reverse
from user_management.models import Profile


class ArticleCategory(models.Model):
    '''
    Model for blog categories

    categories have names and descriptions, ordered by name
    '''
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:article_list', args=[str(self.name)])

    class Meta:
        ordering = ['name']
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'


class Article(models.Model):
    '''
    Model for blog articles

    has foreign key to profile model and ArticleCategory model
    '''
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='blog')
    category = models.ForeignKey(ArticleCategory,
                                 on_delete=models.SET_NULL,
                                 null=True, related_name='blog')
    entry = models.TextField()
    header_image = models.ImageField(upload_to='header/', null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[str(self.pk)])

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class Comment(models.Model):
    '''
    Model for blog comments

    has foreign key to profile that commented and the article
    '''
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='blog_comments')
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                null=True, related_name='blog_comments')
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entry

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class ArticleImage(models.Model):
    '''
    Model for article images, used for the gallery for blog articles

    has foreign key to article
    '''
    image = models.ImageField(upload_to='images/', null=True)
    description = models.TextField(max_length=255)
    article = models.ForeignKey(Article,
                               on_delete=models.CASCADE,
                               related_name="blog_images")
    