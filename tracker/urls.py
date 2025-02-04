from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard, name="home"),
    path("calendar/", views.calendar_view, name="calendar"),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar'),
    path("add/followup/", views.add_followup, name="add_followup"),
    path("add/evangelism/", views.add_evangelism, name="add_evangelism"),
]
