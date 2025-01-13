from django.db import transaction
from .models import Evangelism, FollowUp
from datetime import date, timedelta

def create_evangelism(user, person_name, description, faith, course=None, evangelism_date=None, location=None):
    """
    Creates an evangelism record and schedules follow-ups.
    """
    # Create and save the Evangelism instance
    with transaction.atomic():
        evangelism = Evangelism(
            evangelist=user,
            person_name=person_name,
            description=description,
            faith=faith,
            location=location,
            course=course,
            date=evangelism_date if evangelism_date else date.today()
        )
        evangelism.save()

        # Create follow-up instances
        followups = []
        interval_days = Evangelism.objects.all().count() # relies on the total no. of evangelism
        first_date = Evangelism.objects.order_by("date").first().date
        interval_date = timedelta(interval_days)

        for i in range(7):  # Create 7 follow-ups
            if i < 3:
                new_followup = FollowUp(evangelism=evangelism, date=first_date + interval_date)
                followups.append(new_followup)
                interval_date += timedelta(interval_days)
                print(f"Followup{i} date:", new_followup.date, "\n")
            else:
                interval_date += timedelta(2) + timedelta(interval_days)
                new_followup = FollowUp(evangelism=evangelism, date=first_date + interval_date)
                followups.append(new_followup)
                print(f"Followup{i} date:", new_followup.date, "\n")

        # Bulk create follow-ups
        FollowUp.objects.bulk_create(followups)
    return True




def schedule_activity():
    """
    Schedules follow-ups for evangelism records, ensuring they align with the current date.
    """

    if Evangelism.objects.exists():
        for evangelism in Evangelism.objects.all():
            # Get today's follow-ups for this evangelism
            followups = FollowUp.objects.filter(evangelism=evangelism, date=date.today())
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
