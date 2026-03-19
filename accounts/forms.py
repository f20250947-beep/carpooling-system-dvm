from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')
                  #Django ka ready made register form hai jisme username, password1, password2 already hain.
                  #RegisterForm(UserCreationForm) — humne usse extend kiya aur role field bhi add kar di.
#Meta class — Django ko batata hai ki ye form kis model ke liye hai aur kaunse fields dikhane hain.