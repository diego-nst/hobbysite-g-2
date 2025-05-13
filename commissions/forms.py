from django import forms
from .models import Commission, Job

class CommissionForm(forms.ModelForm):
    '''
    Form for the Commission Model
    
    Only contains title, description and status as the rest of the fields should be added automatically
    '''

    class Meta:
        model = Commission
        fields = ['title', 'description', 'status']

        OPEN = "A"
        FULL = "B"
        COMPLETED = "C"
        DISCONTINUED = "D"
        STATUS_CHOICES = {
            OPEN: "Open",
            FULL: "Full",
            COMPLETED: "Completed",
            DISCONTINUED: "Discountinued",
        }
        widgets = {
            'status': forms.Select(choices=STATUS_CHOICES,)
        }


class JobForm(forms.ModelForm):
    '''
    Form for the Job Model
    
    Only contains role and manpowerRequired as the rest of the fields should be added automatically
    '''
    class Meta:
        model = Job
        fields = ['role', 'manpowerRequired']
