from django import forms
from django.utils import timezone
from django.utils.encoding import smart_str

from ..models import Category


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['parent', 'title', 'description', 'color']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = (
            Category.objects
                .visible()
                .parents()
                .ordered()
        )
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        self.fields['parent'] = forms.ModelChoiceField(queryset=queryset, required=False)

        self.fields['parent'].label_from_instance = (lambda obj: smart_str(obj.title))

    def clean_parent(self):
        parent = self.cleaned_data["parent"]

        if self.instance.pk:
            has_children = self.instance.category_set.all().exists()

            if parent and has_children:
                raise forms.ValidationError(
                    ("The category you are updating "
                     "can not have a parent since it has children"))

        return parent

    def save(self, commit=True):
        self.instance.modified = timezone.now()
        return super().save(commit)


class EditCategoryForm(AddCategoryForm):
    pass
