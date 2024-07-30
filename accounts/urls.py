from django.urls import path 
from .views import SignUpView
from . import views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('process_donation/', views.process_donation, name='process_donation'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('password_change/', views.password_change, name='password_change'),
]

