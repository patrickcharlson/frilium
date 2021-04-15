from django.contrib.auth import get_user_model
from django.shortcuts import render

from ...categories.models import Category
from ...core.utils.decorators import administrator_required
from ...posts.models import Post
from ...topics.models import Topic

User = get_user_model()


@administrator_required
def dashboard(request):
    context = {
        'category_count': Category.objects.all().count(),
        'topic_count': Topic.objects.all().count(),
        'posts_count': Post.objects.all().count(),
        'users_count': User.objects.all().count()
    }
    return render(request, 'frilium/admin/dashboard.html', context)
