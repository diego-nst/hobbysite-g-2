from django.db import models
from django.urls import reverse
from user_management.models import Profile


class ArticleCategory(models.Model):
    '''
    This model is for the different categories of the articles.

    Fields include name and description of the category.
    '''
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wiki:article_category', args=[str(self.name)])

    class Meta:
        ordering = ['name']
        verbose_name = 'Article Category'
        verbose_name_plural = 'Article Categories'


class Article(models.Model):
    '''
    This model is for the articles themselves.

    Fields include title, author, category (foreign key to ArticleCategory), entry, header_image, created on, and updated on.
    '''
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, related_name='wikis')
    category = models.ForeignKey(ArticleCategory,
                                 on_delete=models.SET_NULL,
                                 null=True, related_name='wikis')
    entry = models.TextField()
    header_image = models.ImageField(upload_to='header/', null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wiki:wiki_detail', args=[str(self.pk)])

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


class Comment(models.Model):
    '''
    This model is for the comments on the articles.

    Fields include author, article(foreign key to Article), entry, created on, and updated on.
    '''
    author = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, related_name='author_comment')
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                null=True, related_name='wiki_comment')
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
    This model is for the images in the image gallery

    Fields include image, description, and article(foreign key to Article).
    '''
    image = models.ImageField(upload_to='images/', null=True)
    description = models.TextField(max_length=255)
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                related_name="wiki_images")

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
