from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    fields = [
        'username'
        'first_name',
        'email',
        'password1',
        'password2',
    ]


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput (attrs={'class': 'form-control', 'readonly': False}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': False}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': False}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'readonly': True}), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'readonly': True}), required=False)
    class Meta:
        model = User
        fields = (
            'first_name',
            'password1',
            'password2',
            'last_name',
            'email'
        )


class UserPasswordChangeForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
