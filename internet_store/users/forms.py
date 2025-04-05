from .models import Users
from django.forms import ModelForm, TextInput, PasswordInput, EmailInput

class UsersForm(ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'password', 'email', 'card_number']

        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'First name'
            }),
            'last_name': TextInput(attrs={
                'placeholder': 'Last name'
            }),
            'password': PasswordInput(attrs={
                'placeholder': 'Password',
                'name':'password'
            }),
            'email': EmailInput(attrs={
                'placeholder': 'Email',
                'name':'email'
                
            }),
            'card_number': TextInput(attrs={
                'placeholder': '0000 0000 0000 0000'
            })
        }