from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.utils.http import url_has_allowed_host_and_scheme

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(label="Email address", widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    redirect_url = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = User
        fields = ['username']

    def __init__(self, host=None, *args, **kwargs):
        self.host = host
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'username'})

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        if url and url_has_allowed_host_and_scheme(url, self.host):
            return url
        return settings.LOGIN_REDIRECT_URL

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class SignupForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': 'The two password fields don’t match.',
    }

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        strip=False, )

    class Meta:
        model = User
        fields = ('email', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        is_taken = User.objects.filter(username=username).exists()
        if is_taken:
            raise forms.ValidationError('The above username is not available!')
        return self.cleaned_data['username']

    def clean_email(self):
        email = self.cleaned_data['email']
        is_taken = User.objects.filter(email=email).exists()
        if is_taken:
            raise forms.ValidationError('The above email is taken!')
        return self.cleaned_data['email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class SignInForm(AuthenticationForm):
    username = forms.EmailField(label="Email address", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    redirect_url = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, host, *args, **kwargs):
        self.host = host
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        if url and url_has_allowed_host_and_scheme(url, self.host):
            return url


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

        raise forms.ValidationError("No account matches {}.".format(username))

    def clean(self):
        self.validate_username()
        super().clean()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email', widget=forms.TextInput(attrs={'autofocus': True}))


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None
