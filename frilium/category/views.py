from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from .models import Category
from ..boards.models import Board
from ..thread.models import Topic
from ..thread.private.models import TopicPrivate


@login_required
def board_category(request, slug, pk):
    category = get_object_or_404(Category, slug=slug, pk=pk)
    category_boards = Board.objects.filter(category=category)
    context = {'cat': category, 'boards': category_boards}
    return render(request, 'frilium/category/board-category.html', context)


@login_required
def topic_category(request, slug, pk):
    private_topics = TopicPrivate.objects.all()
    category = get_object_or_404(Category, slug=slug, pk=pk)
    category_topics = Topic.objects.exclude(private_topics__in=private_topics).select_related().filter(
        board__category=category). \
        annotate(replies=Count('posts') - 1).order_by('-date_created')
    context = {'topics': category_topics}
    return render(request, 'frilium/category/topic-category.html', context)
