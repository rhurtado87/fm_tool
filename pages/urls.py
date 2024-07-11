# config/urls.py

from django.urls import path
from pages import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('help/', views.help_support, name='help_support'),
    path('market/', views.market, name='market'),
    path('transactions/', views.transactions, name='transactions'),
]
