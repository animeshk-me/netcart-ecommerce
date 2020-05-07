"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Below two lines handle the 'static files'.
from django.conf.urls.static import static 
from django.conf import settings
from django.views.generic import TemplateView


from django.contrib import admin
from django.urls import path, include
from products.views import product_list_view

from .views import (
    home_view, 
    login_page_view, 
    register_page_view,
    contact_view,
    logout_page_view
)

# from products.views import product_list_view, ProductListView

urlpatterns = [
    path('', home_view, name='home_view'),
    path('admin/', admin.site.urls, name = 'admin_view'),
    path('login/', login_page_view, name ='login'),
    path('logout/', logout_page_view, name ='logout'),
    path('register/', register_page_view, name = 'register'),
    path('contact/', contact_view, name='contact'),
    # path('products-fbv/', product_list_view), #function-based-view (fbv)
    # path('products/', ProductListView.as_view()),
    path('products/', include('products.urls')),
    path('search/', include('search.urls')),
    path('cart/', include('carts.urls')),
    path('profile/', include('profiles.urls')),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)