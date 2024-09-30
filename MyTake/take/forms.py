from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class InputForm(forms.Form):
    user_input = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Ask ChatGPT...'}), label='Your question', max_length=500)