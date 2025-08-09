from django import forms
from .models import FollowUp, Evangelism


class FollowUpForm(forms.ModelForm):
    completed = forms.BooleanField()
    class Meta:
        model = FollowUp
        fields = ["evangelism", "description", "date", "completed"]
    
    def save(self, commit=True):
        followup = super().save(commit=commit)
        followup.evangelism.completed = self.cleaned_data['completed']
        if commit:
            followup.evangelism.save()
        return followup


    



class EvangelismForm(forms.ModelForm):
    date = forms.DateField()
    
    class Meta:
        model = Evangelism
        fields = ["person_name", 
                  "course", 
                  "location", 
                  "date", 
                  "description", 
                  "faith",
                  "completed"]