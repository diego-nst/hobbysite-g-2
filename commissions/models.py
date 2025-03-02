from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    peopleRequired = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('commissions:commissions/detail', args = [self.pk])



class Comment(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.SET_NULL, null=True, related_name='comment')
    entry = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)