from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from frilium.boards.models import Board
from frilium.category.models import Category
from frilium.thread.models import Topic


@login_required
def board_category(request, slug, pk):
    category = get_object_or_404(Category, slug=slug, pk=pk)
    category_boards = Board.objects.filter(category=category)
    context = {'cat': category, 'boards': category_boards}
    return render(request, 'frilium/category/board-category.html', context)


@login_required
def topic_category(request, slug, pk):
    category = get_object_or_404(Category, slug=slug, pk=pk)
    category_topics = Topic.objects.select_related().filter(board__category=category). \
        annotate(replies=Count('posts') - 1).order_by('-date_created')
    context = {'topics': category_topics}
    return render(request, 'frilium/category/topic-category.html', context)
