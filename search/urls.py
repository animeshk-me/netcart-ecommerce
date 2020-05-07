from django.urls import path
from .views import (
    search_product_list_view
)


app_name = 'search'       #namespace declaration

urlpatterns = [
    path('', search_product_list_view, name = 'search'),
]