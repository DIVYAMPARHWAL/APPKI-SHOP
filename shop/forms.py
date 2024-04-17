from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django import forms
from .models import Item as Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['user', 'items']


class CreateUserForm(UserCreationForm):
    company_name=forms.CharField(max_length=20)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2','company_name']