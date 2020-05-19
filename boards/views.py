from django.views.generic import ListView

from boards.models import Board


class BoardListView(ListView):
    model = Board
    context_object_name = 'board_list'
    template_name = 'home.html'
