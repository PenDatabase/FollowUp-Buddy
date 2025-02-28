from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.UserSignUpView.as_view(), name="signup"),
    path('login/', views.UserLoginView.as_view(), name='login')
]