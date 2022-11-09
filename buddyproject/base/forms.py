from django.forms.models import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from base.models import Room, User
from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User    
        fields = ['avatar', 'name', 'username', 'email', 'bio']


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2', 'avatar', 'bio']


class AuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

   
