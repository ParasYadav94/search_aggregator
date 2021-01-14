from django.urls import path
from product_search.views import search

app_name = 'product'

urlpatterns = [
    path('', search, name="search"),
]