from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from .models import Category
from ..topics.models import Topic
from ..topics.private.models import TopicPrivate

private_topics = TopicPrivate.objects.all()


@login_required
def view_category(request, slug, pk):
    category = get_object_or_404(Category, slug=slug, pk=pk)
    subcategories = Category.objects.children(parent=category)
    topics = (Topic.objects
              .for_category(category=category)
              .exclude(private_topics__in=private_topics)
              .annotate(replies=Count('posts') - 1)
              .select_related('category')
              .order_by('-date_created'))

    context = {'c': category,
               'subcategories': subcategories,
               'topics': topics}
    return render(request, 'frilium/categories/view.html', context)


@login_required
def list_categories(request):
    categories = Category.objects.all()

    context = {'categories': categories}
    return render(request, 'frilium/categories/categories.html', context)
