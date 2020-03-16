from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.contrib.auth.models import User

class CustomerForm(ModelForm):
    class Meta:
        model = customer
        fields = '__all__'
        exclude = ['user']

class orderForm(ModelForm):
    """docstring for orderForm."""
    class Meta:
        # this is given for the model name which has to be created
        model = order
        # below tag can be specified in model like mentioning the model names in form
        # her all is given so that we can make form for all the feilds
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
