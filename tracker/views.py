from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.generic import CreateView, ListView, TemplateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from datetime import datetime
from calendar import monthrange
from .utils import recommend_activity
from .models import Evangelism, FollowUp
from .forms import EvangelismForm, FollowUpForm
from django.db.models import Count




class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tracker/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
    
        context["followup"] = recommend_activity(evangelist=user)

        context["total_evangelism"] = Evangelism.objects.filter(evangelist=user).count()
        context["total_followup"] = FollowUp.objects.filter(evangelism__evangelist=user).count()
        return context
    



class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'tracker/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get year and month from URL parameters or use current date
        year = kwargs.get('year')
        month = kwargs.get('month')
        
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
            if Evangelism.objects.filter(date=date, evangelist=self.request.user).exists() or FollowUp.objects.filter(date=date, evangelism__evangelist=self.request.user).exists():
                has_activity = True
            else:
                has_activity = False
            calendar_days.append({
                'day': day,
                'date': date.strftime('%Y-%m-%d'),
                'has_activity': has_activity
            })

        # Calculate previous and next months
        prev_month = (month - 1) if month > 1 else 12
        prev_year = year if month > 1 else year - 1

        next_month = (month + 1) if month < 12 else 1
        next_year = year if month < 12 else year + 1

        context.update({
            'month': datetime(year, month, 1).strftime('%B'),
            'year': year,
            'calendar_days': calendar_days,
            'placeholders': placeholders,
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year
        })
        return context





class EvangelismListing(LoginRequiredMixin, ListView):
    template_name = "tracker/evangelism_listing.html"
    context_object_name = "evangelisms"

    def get_queryset(self):
        # Annotate with number of followups for display in listing
        return (
            Evangelism.objects.filter(evangelist=self.request.user)
            .annotate(followup_count=Count("followups"))
            .order_by("-date")
        )
    



class AddEvangelism(LoginRequiredMixin, CreateView):
    form_class = EvangelismForm
    template_name = "tracker/add_evangelism.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.evangelist = self.request.user
        return super().form_valid(form)
    

class AddFollowUp(LoginRequiredMixin, CreateView):
    form_class = FollowUpForm
    template_name = "tracker/add_followup.html"
    success_url = reverse_lazy("home")

    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        form.fields["evangelism"].queryset = Evangelism.objects.filter(evangelist= self.request.user)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form(self.form_class)
        context["evangelisms"] = form.fields["evangelism"].queryset
        return context



class EvangelismDetail(LoginRequiredMixin, DetailView):
    model = Evangelism
    template_name = "tracker/evangelism_detail.html"
    context_object_name = "evangelism"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followups"] = FollowUp.objects.filter(evangelism=self.object)
        return context
    
    
    

class ActivitiesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        date = request.GET.get("date")
        if date:
            evangelisms = [
                {
                    "person_name": e.person_name,
                    "faith": e.faith,
                    "detail_link": reverse("evangelism-detail", args=[e.pk])
                }
                for e in Evangelism.objects.filter(date=date, evangelist=request.user)
            ]

            followups = list(FollowUp.objects.filter(date=date, evangelism__evangelist=request.user).values(
                "evangelism__person_name", "description"
            ))

            return JsonResponse({
                "evangelisms": evangelisms,
                "followups": followups
            })
        
        return JsonResponse({"evangelisms": [], "followups": []})