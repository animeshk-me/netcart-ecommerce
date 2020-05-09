from django.contrib import admin

from .models import UserStripe, UserAddress

admin.site.register(UserStripe)

class UserAddressAdmin(admin.ModelAdmin):
    class Meta:
        model = UserAddress

admin.site.register(UserAddress, UserAddressAdmin)