from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import User


# Sign Up Form
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'birthdate',
            'gender',
            'profile_picture',
            'email',
            'password1', 
            'password2'
            ]