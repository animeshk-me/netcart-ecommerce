from django.shortcuts import render
# Create your views here.
from .models import Profile
from .forms import ProfileForm, ProfileModelform




def profile_view(request):
    prof_obj = Profile.objects.get(user=request.user)
    print('profview')
    print(prof_obj)
    context = {
        'profile' : prof_obj
    }
    return render(request, 'profile.html', context)
    


def profile_form_view(request):
 
    form = ProfileForm(request.POST or None)
    context = {
        'profile_form' : form
    }
    print('out')
    print(form.errors)
    print(form.is_valid())
    if form.is_valid():
        print('ho')
        prof_obj = Profile.objects.get(user=request.user)
        print('hi')
        print(prof_obj)
        print(form)
        prof_obj.firstname = form.cleaned_data.get('lastname')
        prof_obj.lastname  = form.cleaned_data.get('lastname')
        prof_obj.address1  = form.cleaned_data.get('address1')
        prof_obj.address2  = form.cleaned_data.get('address2')
        prof_obj.phone     = form.cleaned_data.get('phone')
    return render(request, 'profile_form.html', context)