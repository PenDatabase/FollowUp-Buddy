from django import forms
from .models import FollowUp, Evangelism


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = "__all__"



class EvangelismForm(forms.ModelForm):
    date = forms.DateField()
    class Meta:
        model = Evangelism
        fields = ["person_name", 
                  "course", 
                  "location", 
                  "date", 
                  "description", 
                  "faith"]