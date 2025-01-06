from django.db import models
from django.contrib.auth.models import User


class Evangelism(models.Model):
    FAITH_STATUS = {
        "strong_faith": "Strong Faith",
        "less_faith": "Less Faith",
        "unbeliever": "unbeliever"
    }
    evangelist = models.ForeignKey(User, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    faith = models.CharField(choices=FAITH_STATUS)




class FollowUp(models.Model):
    evangelism = models.ForeignKey(Evangelism, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField()
