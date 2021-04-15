from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

User = get_user_model()


class UserForm(ModelForm):
    bio = forms.CharField(label='Bio', widget=forms.Textarea(attrs={'rows': 7}), required=False)

    class Meta:
        model = User
        fields = ['name', 'gender', 'is_admin', 'is_mod', 'bio', 'location', 'website']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].required = False
        self.fields['website'].initial = 'https://'


class UserBaseForm(ModelForm):
    username = forms.CharField(label='Username')
    email = forms.CharField(label='E-mail address')

    class Meta:
        model = User
        fields = ['username', 'email']

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


class NewUserForm(UserBaseForm):
    error_messages = {
        'password_mismatch': 'The two password fields don’t match.',
    }

    new_password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput)
    confirm = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_new_password(self):
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('confirm')
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )


class AdminAuthenticationForm(AuthenticationForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.error_messages.update(
            {"not_staff": "Your account does not have admin privileges."}
        )
        super().__init__(*args, **kwargs)

    def confirm_login_allowed(self, user):
        if not user.is_staff:
            raise ValidationError(
                self.error_messages['not_stuff'], code='not_stuff'
            )
