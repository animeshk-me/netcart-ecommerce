from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout

from .forms import LoginForm, RegisterForm
from profiles.models import Profile 
from accounts.models import UserAddress,UserDefaultAddress

def home_view(request):
    return redirect('products_url:show_all_products')

def login_page_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/products')
        else:
            print('error')
    context = {
        'login_form': form
    }
    return render(request, 'auth/login_page.html', context)
    


User = get_user_model()

def register_page_view(request):
    form = RegisterForm(request.POST or None)
    context = {
        'register_form': form
    }
    if(form.is_valid()):
        print(form.cleaned_data)
        username  = form.cleaned_data.get('username')
        email     = form.cleaned_data.get('email')
        password  = form.cleaned_data.get('password')
        # firstname = form.cleaned_data.get('firstname')
        # lastname  = form.cleaned_data.get('lastname')
        # address1  = form.cleaned_data.get('address1')
        # address2  = form.cleaned_data.get('address2')
        # phone     = form.cleaned_data.get('phone')
        new_user  = User.objects.create_user(username, email, password)
        #now, here if you make it (email, username, password) like this it will automatically take emails as usernames.
        print(new_user)
        login(request, new_user)
        prof_obj           = Profile.objects.create(user=request.user)
        prof_obj.firstname = form.cleaned_data.get('firstname')
        prof_obj.lastname  = form.cleaned_data.get('lastname')
        prof_obj.address1  = form.cleaned_data.get('address1')
        prof_obj.address2  = form.cleaned_data.get('address2')
        prof_obj.phone     = form.cleaned_data.get('phone')
        prof_obj.save()
        def_address         = UserAddress.objects.create(user=request.user)
        def_address.address = prof_obj.address1
        def_address.address2= prof_obj.address2
        def_address.phone   = prof_obj.phone
        def_address.shipping= True
        def_address.billing = True
        def_address.city    = form.cleaned_data.get('city')
        def_address.state   = form.cleaned_data.get('state')
        def_address.country = form.cleaned_data.get('country')
        def_address.zipcode = form.cleaned_data.get('zipcode')
        def_address.save()
        temp, created       = UserDefaultAddress.objects.get_or_create(user=request.user)
        temp.billing        = def_address
        temp.shipping       = def_address
        temp.save()
    return render(request, 'auth/register_page.html', context)
    
def contact_view(request):
    return render(request, 'hometemp/contact.html', {})


def logout_page_view(request):
    logout(request)
    return redirect('/products')