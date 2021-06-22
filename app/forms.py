from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import (authenticate, get_user_model, password_validation,)
from app.models import customer,product

class myregistrationform(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label='Conform Password')
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}),required=True)
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        widgets={
            'username':forms.EmailInput(attrs={'class':'form-control'})
        }
        labels={'email':'Email','username':'User Name'}






class myloginform(AuthenticationForm):
    '''for sign in of user'''
    username = UsernameField(widget=forms.TextInput(attrs={'class':'form-control','autofocus': True}),label='Name')
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete': 'current-password'}),
    )




class signinuser1(AuthenticationForm):
    class Meta:
        model=User
        fields=['username','password']
        widgets={'username':forms.TextInput(attrs={'class':'form-control'}),'password':forms.TextInput(attrs={'class':'form-control'})}



class mypasswordchangeform(PasswordChangeForm):
    '''for password change'''
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Conform New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete': 'new-password'}),
    )


class mypasswordresetform(PasswordResetForm):
    '''for password reset form'''
    email = forms.EmailField(
        label=_("Enter your Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'class':'form-control','autocomplete': 'email'})
    )



class mysetpasswordform(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete': 'new-password'}),
    )





class addressform(forms.ModelForm):
    # address1=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),label='Address 1')
    # address2=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),label='Address 2')
    class Meta:
        model=customer
        fields=['name','locality','city','state','zipcode']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'})}



class productaddform(forms.ModelForm):
    class Meta:
        model=product
        fields=['title','selling_price','discount_price','description','brand','catagory','product_image']
        widgets={
        'title':forms.TextInput(attrs={'class':'form-control'}),
        'selling_price': forms.TextInput(attrs={'class': 'form-control'}),
        'discount_price': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.TextInput(attrs={'class': 'form-control'}),
        'brand': forms.TextInput(attrs={'class': 'form-control'}),
        'catagory': forms.Select(attrs={'class': 'form-control'}),
        'product_image': forms.FileInput(attrs={'class': 'form-control'})}
