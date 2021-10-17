from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    message = forms.CharField(label='', widget=forms.Textarea())

    class Meta:
        model = Post
        fields = ['message', ]

    def __init__(self, *args, user=None, topic=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.topic = topic

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.user = self.user
            self.instance.topic = self.topic
        return super(PostForm, self).save()


class EditPostForm(PostForm):
    pass
