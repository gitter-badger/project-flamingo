from django import forms

from django.contrib.auth import get_user_model
MyUser = get_user_model()


class LoginForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'password']


class SignUpForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'password']
