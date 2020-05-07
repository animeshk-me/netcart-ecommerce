from django.urls import path

from .views import profile_form_view, profile_view

app_name = 'profile'

urlpatterns = [
    path('', profile_view, name = 'profile'),
    path('update', profile_form_view, name = 'profile_update'),
]