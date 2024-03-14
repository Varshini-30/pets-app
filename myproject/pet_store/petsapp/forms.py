from django import forms
from .models import log, ShippingAddress1
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class login(forms.ModelForm):
    class Meta:
        model = log
        fields = ('name', 'email', 'phone')


# class signupform(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email']

class SearchForm(forms.Form):
    q = forms.CharField(label='search', max_length=50)


class ShippingAddress1Form(forms.ModelForm):
    class Meta:
        model = ShippingAddress1
        fields = ['building_name', 'street',
                  'landmark', 'city', 'state', 'zipcode']

class SetDeliveryAddressForm(forms.Form):
    delivery_address=forms.CharField()