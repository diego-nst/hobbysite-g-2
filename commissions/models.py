from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    peopleRequired = models.IntegerField(
        default=0, validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commission-detail', args=[self.pk])

    class Meta():
        ordering = ['created']
        verbose_name = "Commission"


class Comment(models.Model):
    commission = models.ForeignKey(
        Commission, on_delete=models.CASCADE, null=True, related_name='comments')
    entry = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta():
        ordering = ['-created']
        verbose_name = "Comment"
