from django.utils import timezone
from .models import Evangelism

def recommend_activity():
    evangelisms = Evangelism.objects.filter(completed=False).select_related("followup").order_by("date")

    if evangelisms.count() >= 7:
        for evangelism in evangelisms:
            if evangelism.followup:
                last_followup = evangelism.followup_set.order_by("date").last()
                if ((timezone.now().date() - last_followup.date) >= 7):
                    return evangelism
            else:
                if ((timezone.now().date() - evangelism.date) >= 7):
                    return evangelism
    
    return None

