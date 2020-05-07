from django import forms
from .models import Profile



class ProfileModelform(forms.ModelForm):
    firstname = forms.CharField(widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your First Name',
                    'class' : 'form-control'
                    }))
    lastname  = forms.CharField(widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your Second Name',
                    'class' : 'form-control'
                    }))
    address1  = forms.CharField(widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your address',
                    'class' : 'form-control'
                    }))
    address2  = forms.CharField(widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your secondary address',
                    'class' : 'form-control'
                    }))              
    phone     = forms.IntegerField(max_value = 10000000000)
    
    class Meta:
        model = Profile
        fields = (
            "firstname",
            "lastname",
            "address1",
            "address2",
            "phone"
        )


class ProfileForm(forms.Form):

    firstname = forms.CharField(widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your First Name',
                    'class' : 'form-control'
                    }))
    lastname  = forms.CharField(widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your Second Name',
                    'class' : 'form-control'
                    }))
    address1  = forms.CharField(widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your address',
                    'class' : 'form-control'
                    }))
    address2  = forms.CharField(widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your secondary address',
                    'class' : 'form-control'
                    }))              
    phone     = forms.IntegerField(max_value = 10000000000)
    

    def clean_data(self, request):
        return self.cleaned_data
