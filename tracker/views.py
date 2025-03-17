from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView, ListView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from datetime import datetime
from calendar import monthrange
from .utils import recommend_activity
from .models import Evangelism, FollowUp
from .forms import EvangelismForm, FollowUpForm




@login_required
def dashboard(request):
    context = {}
    if request.user.is_authenticated:
        activity = recommend_activity(evangelist=request.user)
    else:
        activity = recommend_activity()
    if activity is not None:
        context["followup"] = activity
    

    context["total_evangelism"] = Evangelism.objects.filter(evangelist=request.user).count()
    context["total_followup"] = FollowUp.objects.filter(evangelism__evangelist=request.user).count()

    return render(request, "tracker/home.html", context)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tracker/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if self.request.user.is_authenticated:
            context["followup"] = recommend_activity(evangelist=user)
        else:
            context["followup"] = recommend_activity()

        context["total_evangelism"] = Evangelism.objects.filter(evangelist=user).count()
        context["total_followup"] = FollowUp.objects.filter(evangelism__evangelist=user).count()
        return context
    



@login_required
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
        if Evangelism.objects.filter(date=date).exists() or FollowUp.objects.filter(date=date).exists():
            has_evangelism = True
        else:
            has_evangelism = False
        calendar_days.append({
            'day': day,
            'date': date.strftime('%Y-%m-%d'),
            'has_evangelism': has_evangelism
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



class EvangelismListing(LoginRequiredMixin, ListView):
    template_name = "tracker/evangelism_listing.html"
    context_object_name = "evangelisms"

    def get_queryset(self):
        return Evangelism.objects.filter(evangelist= self.request.user).all()
    


class AddEvangelism(LoginRequiredMixin, CreateView):
    form_class = EvangelismForm
    template_name = "tracker/add_evangelism.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.evangelist = self.request.user
        return super().form_valid(form)
    


@login_required
def add_followup(request):
    if request.method == "POST":
        followup = FollowUpForm(request.POST, evangelist=request.user)

        if followup.is_valid():
            followup.save()
            return redirect("home")

    form = FollowUpForm(evangelist=request.user)
    evangelisms = Evangelism.objects.filter(evangelist=request.user).all()
    context = {
        "form": form,
        "evangelisms": evangelisms
    }
    return render(request, "tracker/add_followup.html", context)