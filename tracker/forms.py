from django import forms
from .models import FollowUp, Evangelism


class FollowUpForm(forms.ModelForm):
    completed = forms.BooleanField(required=False)
    class Meta:
        model = FollowUp
        fields = ["evangelism", "description", "date", "completed"]
    
    def save(self, commit=True):
        followup = super().save(commit=commit)
        completed_value = self.cleaned_data.get("completed")
        if completed_value is not None:
            followup.evangelism.completed = completed_value
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