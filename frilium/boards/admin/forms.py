from django.forms import ModelForm

from ...boards.models import Board


class AddBoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description', 'color']


class EditBoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description', 'color']
