from django import forms
from django.contrib.auth.models import User
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from .models import Profile

import stripe
class LoginForm(forms.Form):
    username=forms.CharField(max_length=50,label='Username',label_suffix="",widget=forms.TextInput(attrs={"id":"username"}))
    
    password=forms.CharField(max_length=50,label='Password',label_suffix="",widget=forms.PasswordInput(attrs={"id":"password"}))
    
class SignupForm(forms.ModelForm):
    country = CountryField().formfield()
    class Meta:
        model=User
        fields=[
            'first_name',
            'last_name',
            'username',
            
            'email',
            'password',
            'country',
            
        ]
        # widgets={'country':CountrySelectWidget()}
    def save(self,commit=True):
        print("Before first commit")
        user = super(SignupForm,self).save(commit=False)
        print("First commit completed")
        user.set_password(self.cleaned_data["password"])
        # p=Profile.objects.create(user=user,country=self.cleaned_data['country'])
        if commit:
            print("Second commit initiated")
            user.save()
            customer=stripe.Customer.create(
            email=user.email,
            name=user.get_full_name(),
            metadata={
                'user_id':user.pk,
                'username':user.username
            },
            description="Created from django",
            )
            try:
                account= stripe.Account.create(
                    type="custom",
                    country=self.cleaned_data['country'],
                    email=user.email,
                    capabilities={
                        "card_payments":{"requested":True},
                        "transfers":{"requested":True}
                    }
                    
                )
            except:
                user.delete()
                customer.delete()
                return "We do not support payouts in your country"        
        profile=Profile.objects.create(user=user,stripe_customer_id=customer.id,stripe_account_id=account.id)
        print("profile Created")
        profile.save()
        print("Second commit completed")
        
        return user
class ThreadCreationForm(forms.Form):
    Price=forms.IntegerField(label='Buy out',label_suffix='',widget=forms.TextInput(attrs={"id":"price_input"}))

