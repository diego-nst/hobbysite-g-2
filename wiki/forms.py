from django import forms
from .models import Article, ArticleCategory


class WikiForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'entry', 'category', 'entry', 'header_image']
        widgets = {
            'category': forms.Select(choices=ArticleCategory.objects.all,)
        }

