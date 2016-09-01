from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


from .models import MyUser, Profile


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name']


class MyUserChangeForm(UserChangeForm):
    last_login = forms.DateTimeField(disabled=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'first_name', 'last_name', 'is_staff', 'is_active')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'birthdate', 'rating', 'follows')

    def clean_follows(self):
        user = self.cleaned_data['user']
        following = self.cleaned_data['follows']
        following = [f.user_id for f in following]
        if user.id in following:
            raise forms.ValidationError("User cannot follow self.")
        return self.cleaned_data['follows']

