from django import forms
from .models import User, Rooms
from django.contrib.auth.forms import UserCreationForm

class RoomCreationForm(forms.ModelForm):
    topic = forms.CharField(max_length=200)
    class Meta:
        model = Rooms
        fields = ['name', 'topic', 'description']

class MyUserCreationform(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'bio', 'avatar']