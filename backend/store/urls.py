from django.urls import path
from .views import home_view, search_products

urlpatterns = [
    path('', home_view, name='home'),
    path('search-products/', search_products, name='search_products'),
]