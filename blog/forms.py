from django import forms
from .models import Article, ArticleCategory, Comment


class WikiForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'entry', 'category', 'header_image']
        widgets = {
            'category': forms.Select(choices=ArticleCategory.objects.all,)
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']