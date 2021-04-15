from django import forms

from frilium.apps.posts.report.models import Report


class ReportForm(forms.ModelForm):
    subject = forms.CharField(label='Subject', initial='Report Content', max_length=80)

    class Meta:
        model = Report
        fields = ['subject', 'reason', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reason'].label = 'Choose a reason for reporting this content'
        self.fields['body'].required = True
