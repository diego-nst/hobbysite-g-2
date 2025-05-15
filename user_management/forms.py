from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    '''
    Form for the Profile Model
    
    only contains display name
    used in the update view for profile, where users can only update their display_name
    '''
    class Meta:
        model = Profile
        fields = ['display_name']
