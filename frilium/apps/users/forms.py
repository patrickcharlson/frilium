from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import Form

User = get_user_model()
years = range(1930, datetime.utcnow().year + 1)

YEARS = [x for x in years]


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None


class EmailChangeForm(Form):
    email = forms.CharField(label='New E-mail', widget=forms.EmailInput, max_length=254)
    password = forms.CharField(label='Your current password', widget=forms.PasswordInput)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_email(self):
        email = self.cleaned_data['email']
        is_available = User.objects.filter(email=email).exists()
        if is_available:
            raise forms.ValidationError('This email is being used!!')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError('The provided password is incorrect!!')
        return password

    def save(self, commit=True):
        email = self.cleaned_data['email']
        self.user.email = email
        if commit:
            self.user.save()
        return self.user


class UserForm(forms.ModelForm):
    bio = forms.CharField(label='Bio', widget=forms.Textarea(attrs={'rows': 7}), required=False)
    birthday = forms.DateField(label='Birthday', widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = User
        fields = ['name', 'gender', 'bio', 'location', 'website', 'birthday']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].required = False
        self.fields['website'].initial = 'https://'
