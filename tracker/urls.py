from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard, name="home"),
    path("calendar/", views.calendar_view, name="calendar"),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar'),
    path("evang_select/", views.evang_select, name="evang_select"),
    path("add/followup/<int:pk>", views.add_followup_from_evang, name="add_followup"),
    path("add/evangelism/", views.add_evangelism, name="add_evangelism"),
]
