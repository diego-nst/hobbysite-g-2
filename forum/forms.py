from django import forms

from .models import Thread, Comment


class ThreadForm(forms.ModelForm):
    '''
    This is the form for the Thread model
    '''

    class Meta:
        '''
        The values/data for title, category, entry, and image will be submitted through the forms
        but the date for 'created on' and the author field will be automatically inputted and 
        cannot be edited
        '''
        model = Thread
        fields = ['title', 'category', 'entry', 'image']
        # all fields except created on and author field


class CommentForm(forms.ModelForm):
    '''
    This is the form for the Comment model
    '''

    class Meta:
        '''
        Only the entry field will be available for submission
        '''
        model = Comment
        fields = ['entry',]
