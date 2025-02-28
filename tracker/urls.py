from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard, name="home"),
    path("activity/calendar/", views.calendar_view, name="activity_calendar"),
    path('activity/calendar/<int:year>/<int:month>/', views.calendar_view, name='activity_calendar'),
    path('activity/list/', views.activity_list, name="activity_list"),
    path("add/followup/", views.add_followup, name="add_followup"),
    path("add/evangelism/", views.add_evangelism, name="add_evangelism"),
]
