from django.shortcuts import render, Http404, reverse, HttpResponseRedirect

from .forms import UserAddressForm
from .models import UserDefaultAddress

def add_user_address(request):
    try:
        next_page = request.GET.get("next")
    except:
        next_page = None
    form = UserAddressForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            is_default = form.cleaned_data["default"]
            if is_default:
                default_address, created = UserDefaultAddress.objects.get_or_create(user=request.user)
                default_address.shipping = new_address
                default_address.save()
            else:
                pass
            if next_page is not None:
                return HttpResponseRedirect(reverse(str(next_page))+"?address_added=True")
    submit_btn = "Save Address"
    return render(request, "orders/form.html", {"form":form, "submit_btn": submit_btn})