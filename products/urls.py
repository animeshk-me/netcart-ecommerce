from django.urls import path
from .views import (
    product_detail_view,
    product_list_view,
    featured_list_view,
    product_detail_slug_view
)


app_name = 'products_url'       #namespace declaration

urlpatterns = [
    path('', product_list_view, name = 'show_all_products'),
    path('details/<int:my_id>/', product_detail_view, name = 'product_detail'),
    path('details/<slug:slug>/', product_detail_slug_view, name = 'product_detail_slug'),
    path('featured/', featured_list_view, name = 'featured_list') 

]