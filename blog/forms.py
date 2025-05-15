from django import forms
from .models import Article, ArticleCategory, Comment, ArticleImage


class BlogForm(forms.ModelForm):
    '''
    Form for the Blog Article Model

    Only contains title, entry, category, and header image 
    '''
    class Meta:
        model = Article
        fields = ['title', 'entry', 'category', 'header_image']
        widgets = {
            'category': forms.Select(choices=ArticleCategory.objects.all,)
        }


class CommentForm(forms.ModelForm):
    '''
    Form for the Comment Form

    Contains comment entry
    '''
    class Meta:
        model = Comment
        fields = ['entry']


class ArticleImageForm(forms.ModelForm):
    '''
    Form for ArticleImage, used for the gallery

    Contains ArticleImage and description
    '''
    class Meta:
        model = ArticleImage
        fields = ['image', 'description']
