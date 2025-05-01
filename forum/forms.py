from django import forms 

from .models import Thread, Comment


class ThreadForm(forms.ModelForm):


    class Meta:
        model = Thread
        fields = ['title', 'category', 'entry', 'image']
        # all fields except created on and author field
        
class CommentForm(forms.ModelForm):


    class Meta:
        model = Comment
        fields = ['entry',]


    


