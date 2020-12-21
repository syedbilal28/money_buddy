from django import forms
from django.contrib.auth.models import User
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
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
        user = super(SignupForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
class ThreadCreationForm(forms.Form):
    Price=forms.IntegerField(label='Buy out',label_suffix='',widget=forms.TextInput(attrs={"id":"price_input"}))