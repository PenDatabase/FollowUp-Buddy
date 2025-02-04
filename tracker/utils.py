from django.utils import timezone
from .models import Evangelism

def recommend_activity():
    evangelisms = Evangelism.objects.filter(completed=False).order_by("date")#.select_related("followup_set")

    if evangelisms.count() >= 7:
        for evangelism in evangelisms:
            if evangelism.followup_set.exists():
                last_followup = evangelism.followup_set.order_by("-date").first()
                if (timezone.now().date() - last_followup.date).days >= 7:
                    return last_followup
            else:
                if (timezone.now().date() - evangelism.date).days >= 7:
                    return evangelism
    
    return None

