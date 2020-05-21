from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .forms import NewTopicForm
from .models import Board, Post


class BoardsListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


def board_topics(request, slug):
    board = get_object_or_404(Board, slug=slug)
    return render(request, 'boards/topics.html', {'board': board})


def new_topic(request, slug):
    board = get_object_or_404(Board, slug=slug)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('boards:board_topics', slug=board.slug)
    else:
        form = NewTopicForm()
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})
