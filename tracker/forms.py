from django import forms
from .models import FollowUp, Evangelism


class FollowUpForm(forms.ModelForm):
    completed = forms.BooleanField()
    class Meta:
        model = FollowUp
        fields = ["evangelism", "description", "date", "completed"]
    
    def save(self, commit = ...):
        followup = super().save(commit)
        followup.evangelism.completed = self.completed

    



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