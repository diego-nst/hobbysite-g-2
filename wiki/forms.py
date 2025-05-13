from django import forms
from .models import Article, ArticleCategory, Comment, ArticleImage


class WikiForm(forms.ModelForm):
    '''
    This is the form used in the Create View and Update View either to create or update articles.
    '''
    class Meta:
        model = Article
        fields = ['title', 'entry', 'category', 'header_image']
        widgets = {
            'category': forms.Select(choices=ArticleCategory.objects.all,)
        }


class CommentForm(forms.ModelForm):
    '''
    This is the form used in creating the comments
    '''
    class Meta:
        model = Comment
        fields = ['entry']


class ArticleImageForm(forms.ModelForm):
    '''
    This is the form used to add images into the Image Gallery
    '''
    class Meta:
        model = ArticleImage
        fields = ['image', 'description']
