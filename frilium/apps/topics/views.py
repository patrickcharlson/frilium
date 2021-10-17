from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin

from .forms import EditTopicForm, NewTopicForm
from .models import Topic
from .private.models import TopicPrivate
from ..categories.models import Category
from ..core.viewmodels.views import BaseViewForm
from ..posts.forms import EditPostForm, PostForm
from ..posts.models import Post

private_topics = TopicPrivate.objects.all()


@login_required
def view_topic(request, slug, pk):
    topic = get_object_or_404(Topic.objects.annotate(replies=Count('posts') - 1), slug=slug, pk=pk)
    posts = topic.posts.select_related().order_by('created_at')
    session_key = f'viewed_topic_{topic.slug}'
    if not request.session.get(session_key, False):
        topic.views = F('views') + 1
        topic.save()
        request.session[session_key] = True
    context = {'topic': topic,
               'posts': posts}
    return render(request, 'frilium/topics/view.html', context)


@login_required
def index(request):
    categories = Category.objects.all()
    topics = (Topic.objects
              .exclude(private_topics__in=private_topics)
              .annotate(replies=Count('posts') - 1))

    context = {'categories': categories,
               'topics': topics}
    return render(request, 'frilium/topics/index.html', context)


@login_required
def add_topic(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.category = category
            topic.user = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                user=request.user
            )
            return redirect('frilium:topics:view', slug=topic.slug, pk=topic.pk)
    else:
        form = NewTopicForm()
    context = {'categories': category, 'form': form}
    return render(request, 'frilium/topics/new_topic.html', context)


@login_required
def reply_topic(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, user=request.user, topic=topic)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.user = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()
            url = f'/t/{topic.slug}/{topic.pk}/#p-{post.id}'
            return redirect(url)
    else:
        form = PostForm()
    context = {'form': form, 'topics': topic}
    return render(request, 'frilium/topics/reply_topic.html', context)


class TopicReply(SingleObjectMixin, BaseViewForm):
    model = Post
    template_name = 'frilium/topics/reply_topic.html'

    def get_success_url(self):
        return '{0}?p-{1}'.format(
            reverse(
                'frilium:topics:topic',
                kwargs={
                    'category_slug': self.category_post.topic.category.slug,
                    'category_pk': self.category_post.topic.category.pk,
                    'slug': self.category_post.topic.slug,
                    'pk': self.category_post.topic.pk
                },
            ),
            self.category_post.pk
        )


@login_required
def edit_topic(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    post = topic.posts.first()
    if request.method == 'POST':
        topic_form = EditTopicForm(request.POST, instance=topic)
        post_form = EditPostForm(request.POST, instance=post)

        if topic_form.is_valid() and post_form.is_valid():
            topic = topic_form.save(commit=False)
            post = post_form.save(commit=False)
            topic.last_updated = timezone.now()
            topic.updated_by = request.user
            topic.save()
            post.updated_by = request.user
            post.updated_at = timezone.now()
            post.save()
            url = f'/t/{post.topic.slug}/{post.topic.pk}/#p-{post.id}'
            return redirect(url)
    else:
        topic_form = EditTopicForm(instance=topic)
        post_form = EditPostForm(instance=post)

    context = {'title_form': topic_form, 'post_form': post_form, 'posts': post}
    return render(request, 'frilium/topics/edit_topic.html', context)


@login_required
def show_topic(request, slug, pk):
    topic = get_object_or_404(Topic, slug=slug, pk=pk)
    url = f'{reverse("frilium:boards:topic_post", args=[topic.slug, topic.pk])}'
    return redirect(url)
