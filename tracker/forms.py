from django import forms
from .models import FollowUp, Evangelism


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ["evangelism", "date"]

    def __init__(self, *args, **kwargs):
        evangelist = kwargs.pop('evangelist', None)
        super().__init__(*args, **kwargs)
        self.fields['evangelism'].queryset = Evangelism.objects.filter(evangelist=evangelist)



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