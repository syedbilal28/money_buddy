from django import forms
from django.contrib.auth.models import User
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from .models import Profile,Thread

import stripe
class LoginForm(forms.Form):
    username=forms.CharField(max_length=50,label='Username',label_suffix="",widget=forms.TextInput(attrs={"id":"username"}))
    
    password=forms.CharField(max_length=50,label='Password',label_suffix="",widget=forms.PasswordInput(attrs={"id":"password"}))
class ProfileForm(forms.ModelForm):
    country = CountryField().formfield()
    class Meta:
        model =Profile
        fields=[
            'country',
            'profile_picture'
        ]
    # def save(self,commit=True):

class SignupForm(forms.ModelForm):
    # profile=ProfileForm()
    
    class Meta:
        model=User
        fields=[
            'first_name',
            'last_name',
            'username',
            
            'email',
            'password',
       ]
        # widgets={'country':CountrySelectWidget()}
    def save(self,commit=True):
    #     print("Before first commit")
        user = super(SignupForm,self).save(commit=False)
    #     print("First commit completed")
        user.set_password(self.cleaned_data["password"])
        user.save()
    #     # p=Profile.objects.create(user=user,country=self.cleaned_data['country'])
    #     if commit:
    #         print("Second commit initiated")
    #         user.save()
    #         customer=stripe.Customer.create(
    #         email=user.email,
    #         name=user.get_full_name(),
    #         metadata={
    #             'user_id':user.pk,
    #             'username':user.username
    #         },
    #         description="Created from django",
    #         )
           
        return user
class ThreadCreationForm(forms.ModelForm):
    monthly_charge=forms.IntegerField(label='Buy out',label_suffix='',widget=forms.TextInput(attrs={"id":"price_input"}))
    class Meta:
        model=Thread
        fields=[
            'monthly_charge',
            'privacy',
            'password'
        ]
