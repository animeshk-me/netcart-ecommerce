from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


#from .models import Login_model, Register_model 

class LoginForm(forms.Form):
    # email = forms.EmailField(widget=forms.EmailInput
    #                 (attrs= {
    #                 'placeholder' : 'Your Email',
    #                 'class' : 'form-control',
    #                 'cols' : 20
    #                 }))
    username = forms.CharField(widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'username',
                    'class' : 'form-control'
                    }))
    password = forms.CharField(widget=forms.PasswordInput
                    (attrs= {
                        'placeholder' : 'Enter a secure password',
                        'class' : 'form-control'
                    }))


    # class meta:
    #     model = Login_model
    #     fields = ('email', 'name', 'password')

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if '@' not in email:
    #         raise forms.ValidationError('Invalid Email id')
    #     return email
    
class RegisterForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your First Name',
                    'class' : 'form-control'
                    }))
    email = forms.EmailField(widget=forms.EmailInput
                    (attrs= {
                    'placeholder' : 'Your Email',
                    'class' : 'form-control'
                    }))
    password = forms.CharField(widget=forms.PasswordInput
                    (attrs= {
                        'placeholder' : 'Enter a secure password',
                        'class' : 'form-control'
                    }))

    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput
                    (attrs= {
                        'placeholder' : 'Confirm password',
                        'class' : 'form-control'
                    }))

    firstname = forms.CharField(widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your First Name',
                    'class' : 'form-control'
                    }))
    lastname  = forms.CharField(widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your last Name',
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
    city      = forms.CharField(max_length=120,widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your City',
                    'class' : 'form-control'
                    }))
    state     = forms.CharField(max_length=120,widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your State',
                    'class' : 'form-control'
                    }))
    country   = forms.CharField(max_length=120,widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your Country',
                    'class' : 'form-control'
                    }))
    zipcode   = forms.CharField(max_length=25,widget=forms.TextInput
                    (attrs= {
                    'placeholder' : 'Your Zipcode',
                    'class' : 'form-control'
                    }))           
    phone     = forms.IntegerField(max_value = 10000000000)
    


    # class meta:
    #     model = Login_model
    #     fields = ('email', 'name', 'password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username not allowed")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise forms.ValidationError('Invalid Email id')
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:   
            raise forms.ValidationError("Passwords don't match")
        return data
    