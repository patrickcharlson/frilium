from django import forms

from frilium.category.models import Category


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']


class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']
