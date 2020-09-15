from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .forms import NewTopicForm, EditTopicForm
from .models import Topic
from .private.models import TopicPrivate
from ..boards.models import Board
from ..core.conf import settings
from ..post.forms import PostForm, EditPostForm
from ..post.models import Post

private_topics = TopicPrivate.objects.all()


@login_required
def list_topics(request, slug):
    board = get_object_or_404(Board, slug=slug)
    board_topics = board.topics.exclude(private_topics__in=private_topics).select_related() \
        .order_by('-date_created').annotate(replies=Count('posts') - 1)
    context = {'board': board, 'topics': board_topics}
    return render(request, 'frilium/thread/topics.html', context)


@login_required
def add_topic(request, slug):
    board = get_object_or_404(Board, slug=slug)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.user = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                user=request.user
            )
            return redirect('frilium:post:topic_post', slug=topic.slug, pk=topic.pk)
    else:
        form = NewTopicForm()
    context = {'board': board, 'form': form}
    return render(request, 'frilium/thread/new_topic.html', context)


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
            return redirect(topic.get_absolute_url())
    else:
        form = PostForm()
    context = {'form': form, 'thread': topic}
    return render(request, 'frilium/thread/reply_topic.html', context)


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

    context = {'title_form': topic_form, 'post_form': post_form, 'post': post}
    return render(request, 'frilium/thread/edit_topic.html', context)


@login_required
def show_topic(request, slug, pk):
    topic = get_object_or_404(Topic, slug=slug, pk=pk)
    url = f'{reverse("frilium:boards:topic_post", args=[topic.slug, topic.pk])}'
    return redirect(url)


@login_required
def all_topics(request):
    topics = Topic.objects.exclude(private_topics__in=private_topics,
                                   private_topics__user=request.user).select_related().order_by(
        '-date_created').annotate(replies=Count('posts') - 1)
    return render(request, 'frilium/thread/all_topics.html', context={'topics': topics})


@login_required
def my_topics(request, slug=None):
    if slug:
        board = get_object_or_404(Board, slug=slug)

        topics = Topic.objects.exclude(board_id=settings.TOPIC_PRIVATE_BOARD_PK,
                                       private_topics__in=private_topics).select_related() \
            .filter(board=board, user=request.user).order_by(
            '-date_created').annotate(replies=Count('posts') - 1)
        context = {'topics': topics, 'board': board}
        return render(request, 'frilium/thread/forum_my_topics.html', context)

    topics = Topic.objects.exclude(private_topics__in=private_topics).select_related().filter(
        user=request.user).order_by('-date_created').annotate(
        replies=Count('posts') - 1)
    return render(request, 'frilium/thread/my_topics.html', context={'topics': topics})
