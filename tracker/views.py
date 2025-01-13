from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from calendar import monthrange
from .utils import schedule_activity, create_evangelism
from .models import Evangelism, FollowUp
from .forms import EvangelismForm, FollowUpForm




def dashboard(request):
    context = {}

    activity = schedule_activity()
    if activity != "evangelism":
        context["followup_scheule"] = True
        context["followup"] = activity
    

    context["total_evangelism"] = Evangelism.objects.all().count()
    context["total_followup"] = FollowUp.objects.filter(completed=True).count()

    return render(request, "tracker/home.html", context)






def calendar_view(request, year=None, month=None):
    # Get current year and month if not provided
    if year is None or month is None:
        today = datetime.now()
        year = today.year
        month = today.month
    else:
        year = int(year)
        month = int(month)

    # Number of days in the current month
    num_days = monthrange(year, month)[1]

    # First day of the week (0 = Monday, 6 = Sunday)
    first_day_of_week = datetime(year, month, 1).weekday()

    # Placeholder for empty slots in the calendar
    placeholders = list(range(first_day_of_week))

    # Calendar days
    calendar_days = []
    for day in range(1, num_days + 1):
        date = datetime(year, month, day)
        has_followup = FollowUp.objects.filter(completed=True, date=date).exists()
        calendar_days.append({
            'day': day,
            'date': date.strftime('%Y-%m-%d'),
            'has_followup': has_followup
        })

    # Calculate previous and next months
    prev_month = (month - 1) if month > 1 else 12
    prev_year = year if month > 1 else year - 1

    next_month = (month + 1) if month < 12 else 1
    next_year = year if month < 12 else year + 1

    context = {
        'month': datetime(year, month, 1).strftime('%B'),
        'year': year,
        'calendar_days': calendar_days,
        'placeholders': placeholders,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year
    }
    return render(request, 'tracker/calendar.html', context)









@login_required
def add_evangelism(request):
    if request.method == "POST":
        person_name = request.POST.get("person_name").strip()
        description = request.POST.get("description").strip()
        faith = request.POST["faith"]
        evangelist = request.user
        date = request.POST["date"]
        location = request.POST.get("location").strip()
        course = request.POST.get("course").strip()

        evangelism = create_evangelism(
        user=evangelist,
        person_name=person_name,
        description=description,
        faith=faith,
        location=location,
        course=course,
        evangelism_date=date
        )
    
    form = EvangelismForm()
    context = {
        "form":form
    }
    return render(request, "tracker/add_evangelism.html", context)



        
        




# Adding record views
def add_followup(request):
    pass


