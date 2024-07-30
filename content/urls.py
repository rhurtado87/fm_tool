# content/urls.py

from django.urls import path, include
from . import views
from .views import fetch_stock_data

urlpatterns = [
    path('search/', views.search_stock, name='search_stock'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add-to-dashboard/<int:stock_id>/', views.add_to_dashboard, name='add_to_dashboard'),
    path('remove-from-dashboard/<int:stock_id>/', views.remove_from_dashboard, name='remove_from_dashboard'),
    path('select2/', include('django_select2.urls')),
    path('fetch_stock_data/<str:symbol>/<str:period>/', views.fetch_stock_data, name='fetch_stock_data'),
    # other paths as needed
]
