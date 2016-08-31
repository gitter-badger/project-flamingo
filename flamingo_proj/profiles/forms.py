from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField


from .models import MyUser, Profile


class MyUserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Enter the same password as before, for verification.",
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    last_login = forms.DateTimeField(disabled=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'first_name', 'last_name', 'is_staff', 'is_active')

    def clean_password(self):
        return self.initial['password']


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

