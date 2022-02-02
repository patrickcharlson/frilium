from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from .models import Category
from ..topics.models import Topic
from ..topics.private.models import TopicPrivate

private_topics = TopicPrivate.objects.all()


def view_category(request, slug, pk):
    category = get_object_or_404(Category, slug=slug, pk=pk)
    subcategories = Category.objects.children(parent=category)
    topics = (Topic.objects
              .for_category(category=category)
              .annotate(replies=Count('posts') - 1)
              .select_related('category')
              .order_by('-date_created'))

    context = {'c': category,
               'subcategories': subcategories,
               'topics': topics}
    return render(request, 'frilium/categories/view.html', context)


def list_categories(request):
    categories = Category.objects.visible().parents()

    context = {'categories': categories}
    return render(request, 'frilium/categories/categories.html', context)
