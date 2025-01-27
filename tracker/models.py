from django.db import models
from django.contrib.auth.models import User
import datetime


class Evangelism(models.Model):
    FAITH_STATUS = {
        "strong_faith": "Strong Faith",
        "less_faith": "Less Faith",
        "unbeliever": "Unbeliever",
        "unknown": "Unknown",
    }
    evangelist = models.ForeignKey(User, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=200)
    course = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=255, null=True)
    date = models.DateField()
    description = models.TextField()
    faith = models.CharField(max_length=20, choices=FAITH_STATUS)
    relevance = models.IntegerField(default=2)
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.faith == "strong_faith":
            self.relevance = 1
        elif self.faith == "less_faith":
            self.relevance = 2
        elif self.faith == "unknown":
            self.relevance = 3
        else:
            self.relevance = 4
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.evangelist} -> {self.person_name}"




class FollowUp(models.Model):
    evangelism = models.ForeignKey(Evangelism, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)
