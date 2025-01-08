from .models import Evangelism, FollowUp
from datetime import date, timedelta

def create_evangelism(user, person_name, description, faith, course=None, evangelism_date=None):
    """
    Creates an evangelism record and schedules follow-ups.
    """
    # Create and save the Evangelism instance
    evangelism = Evangelism(
        evangelist=user,
        person_name=person_name,
        description=description,
        faith=faith,
        course=course,
        date=evangelism_date if evangelism_date else date.today()
    )
    evangelism.save()

    # Create follow-up instances
    followups = []
    interval_days = Evangelism.objects.all().count() # relies on the total no. of evangelsim

    for i in range(7):  # Create 7 follow-ups
        if i < 3:
            followups.append(FollowUp(evangelism=evangelism, date=interval_days))
            interval_days += timedelta(days=interval_days)
        else:
            interval_days += 2
            followup_date += timedelta(days=interval_days)  # Subsequent follow-ups increased every timeframe of former followup plus to days
            followups.append(FollowUp(evangelism=evangelism, date=followup_date))

    # Bulk create follow-ups
    FollowUp.objects.bulk_create(followups)


def schedule_activity():
    """
    Schedules follow-ups for evangelism records, ensuring they align with the current date.
    """

    if Evangelism.objects.exists():
        for evangelism in Evangelism.objects.all():
            # Get today's follow-ups for this evangelism
            followups = FollowUp.objects.filter(evangelism=evangelism, date=date.today)
            followup_count = followups.count()

            # Handle the count of follow-ups
            if followup_count == 1:
                today_followup = followups.first()
                return today_followup  # Return the single follow-up for today
            
            elif followup_count > 1:
                # Sort by relevance and id, and adjust follow-up dates
                followups = followups.order_by("relevance", "id")
                today_followup = followups.first()  # Most relevant follow-up

                for followup in followups[1:]:
                    followup.date += timedelta(days=5)  # Reschedule subsequent follow-ups to any amount of days later
                    followup.save()

                return today_followup
            

    return "evangelism"
