from django.db import models
from django.urls import reverse


from user_management.models import Profile


class ThreadCategory(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('forum:thread_category', args=[str(self.name)])

    class Meta:
        ordering = ['name']
        verbose_name = 'Thread Category'
        verbose_name_plural = 'Thread Categories'


class Thread(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="threads"
    )
    category = models.ForeignKey(
        ThreadCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="threads"
    )
    entry = models.TextField(null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:thread_detail', args=[str(self.pk)])

    class Meta:
        ordering = ['-created_on',]
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'


class Comment(models.Model):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name="comments", null=True,
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="comments",
    )
    entry = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entry

    class Meta:
        ordering = ('-created_on',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


# Create your models here.
