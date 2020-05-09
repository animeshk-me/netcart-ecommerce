from django.urls import path
from .views import cart_home3, add_to_cart, remove_from_cart

app_name = 'cart_app'

urlpatterns = [
    path('', cart_home3, name = 'cart'),
    path('add', add_to_cart, name = 'add'),
    path('remove', remove_from_cart, name = 'remove'),
    # path('checkout', checkout_view, name = 'checkout'),
]
