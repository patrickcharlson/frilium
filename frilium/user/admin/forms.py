from django import forms
from django.contrib.auth import get_user_model
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
    new_password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']
