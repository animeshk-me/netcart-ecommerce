from django.urls import path
from .views import checkout, orders
from accounts.views import add_user_address

app_name = 'orders'

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('list/', orders, name='user-orders'),
    path('add_user_address/', add_user_address, name='add_user_address'),
]
