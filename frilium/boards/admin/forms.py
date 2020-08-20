from django.forms import ModelForm

from ...boards.models import Board


class AddBoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description', ]


class EditBoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description']
