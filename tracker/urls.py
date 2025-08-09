from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("activity/calendar/", views.CalendarView.as_view(), name="activity_calendar"),
    path('activity/calendar/<int:year>/<int:month>/', views.CalendarView.as_view(), name='activity_calendar'),
    path('evangelism/listing/', views.EvangelismListing.as_view(), name="evangelism-listing"),
    path('evangelism/detail/<int:pk>/', views.EvangelismDetail.as_view(), name="evangelism-detail"),
    path("add/followup/", views.AddFollowUp.as_view(), name="add-followup"),
    path("add/evangelism/", views.AddEvangelism.as_view(), name="add-evangelism"),
    path("activities/", views.ActivitiesView.as_view(), name="activities"),
]
