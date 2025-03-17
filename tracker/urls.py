from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("activity/calendar/", views.calendar_view, name="activity_calendar"),
    path('activity/calendar/<int:year>/<int:month>/', views.calendar_view, name='activity_calendar'),
    path('evangelism/listing/', views.EvangelismListing.as_view(), name="evangelism-listing"),
    path("add/followup/", views.add_followup, name="add_followup"),
    path("add/evangelism/", views.AddEvangelism.as_view(), name="add_evangelism"),
]
