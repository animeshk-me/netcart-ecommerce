from django import forms

from .models import UserAddress

class UserAddressForm(forms.ModelForm):
    default = forms.BooleanField(label='Make Default Shipping', required=False)
    default_billing = forms.BooleanField(label='Make Default Billing', required=False)
    class Meta:
        model = UserAddress
        fields = [
            'address',
            'address2',
            'city',
            'state',
            'country',
            'zipcode',
            'phone',
        ]