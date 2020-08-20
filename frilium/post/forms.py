from django import forms

from frilium.post.models import Post


class PostForm(forms.ModelForm):
    message = forms.CharField(label='', widget=forms.Textarea())

    class Meta:
        model = Post
        fields = ['message', ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user


class EditPostForm(PostForm):
    pass
