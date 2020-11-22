from django import forms
from django.contrib.auth.models import User
class LoginForm(forms.Form):
    username=forms.CharField(max_length=50,label='',widget=forms.TextInput(attrs={"id":"username"}))
    
    password=forms.CharField(max_length=50,label='',widget=forms.PasswordInput(attrs={"id":"password"}))
    
class SignupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[
            'first_name',
            'last_name',
            'username',
            
            'email',
            'password',
            
        ]
    def save(self,commit=True):
        user = super(SignupForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
