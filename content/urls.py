# content/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_stock, name='search_stock'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add-to-wishlist/<int:stock_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:stock_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    # other paths as needed
]
