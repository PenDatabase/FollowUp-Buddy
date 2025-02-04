from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from calendar import monthrange
from .utils import recommend_activity
from .models import Evangelism, FollowUp
from .forms import EvangelismForm, FollowUpForm




def dashboard(request):
    context = {}

    activity = recommend_activity()
    if activity is not None:
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
        form = EvangelismForm(request.POST)

        if form.is_valid():
            evangelism = form.save(commit=False)
            evangelism.evangelist = request.user #Make evangelist current logged in user
            evangelism.save()

        else:
            return render(request, "tracker/add_evangelism.html", context)
        
    
    form = EvangelismForm()
    context = {
        "form":form
    }
    return render(request, "tracker/add_evangelism.html", context)







@login_required
def add_followup(request):
    if request.method == "POST":
        followup = FollowUpForm(request.POST, evangelist=request.user)

        if followup.is_valid():
            followup.save()
            return redirect("home")

    form = FollowUpForm(evangelist=request.user)
    context = {
        "form": form,
    }
    return render(request, "tracker/add_followup.html", context)