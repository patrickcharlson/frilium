from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.forms import ModelForm

User = get_user_model()


class SignupForm(ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_username(self):
        username = self.cleaned_data['username']
        is_taken = User.objects.filter(username=username).exists()
        if is_taken:
            raise forms.ValidationError('The above username is not available!')
        return self.cleaned_data['username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or E-mail', max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = 'The password is not valid'

    def validate_username(self):
        username = self.cleaned_data['username']
        if not username:
            return

        is_found_username = User.objects.filter(username=username).exists()
        if is_found_username:
            return

        is_found_email = User.objects.filter(email=username)
        if is_found_email:
            return

        raise forms.ValidationError(f'No account matches {"username":username}')

    def clean(self):
        self.validate_username()
        super().clean()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email', widget=forms.TextInput(attrs={'autofocus': True}))


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None
