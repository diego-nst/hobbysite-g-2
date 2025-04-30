from django import forms
from .models import Commission, Job, JobApplication

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = []

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title','description','status']

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
            'statues': forms.Select(choices=STATUS_CHOICES,)
        }
