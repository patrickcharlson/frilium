from django import forms
from django.utils.encoding import force_str


class MultipleInput(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            value = ','.join(force_str(v) for v in value)
        else:
            value = ''
        return super().render(name, value, attrs=None, renderer=None)

    def value_from_datadict(self, data, files, name):
        value = data.get(name)

        if value:
            return [v.strip() for v in value.split(',')]
