from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django import forms


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfilaForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class RecoveryForm(UserProfilaForm):
    class Meta:
        model = User
        fields = ['email']
