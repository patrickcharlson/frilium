from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import UpdateView

from .forms import NewTopicForm, PostForm, EditTopicForm, EditPostForm
from .models import Board, Post, Topic, Category

User = get_user_model()


def index(request):
    context = {'boards': Board.objects.all(),
               'categories': Category.objects.all()}
    return render(request, 'home.html', context)


@login_required
def topics_list(request, slug):
    board = get_object_or_404(Board, slug=slug)
    board_topics = board.topics.select_related() \
        .order_by('-date_created').annotate(replies=Count('posts') - 1)
    context = {'board': board, 'topics': board_topics}
    return render(request, 'boards/topics.html', context)


@login_required
def add_topic(request, slug):
    board = get_object_or_404(Board, slug=slug)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('frilium:boards:topic_post', slug=topic.slug, pk=topic.pk)
    else:
        form = NewTopicForm()
    context = {'board': board, 'form': form}
    return render(request, 'boards/new_topic.html', context)


@login_required
def post_list(request, slug, pk):
    topic = get_object_or_404(Topic, slug=slug, pk=pk)
    topic_posts = topic.posts.select_related().order_by('created_at')
    session_key = f'viewed_topic_{topic.slug}'
    if not request.session.get(session_key, False):
        topic.views = F('views') + 1
        topic.save()
        request.session[session_key] = True
    context = {'posts': topic_posts, 'topic': topic}
    return render(request, 'boards/topic_posts.html', context)


@login_required
def board_category(request, slug, pk):
    category = get_object_or_404(Category, slug=slug, pk=pk)
    category_boards = Board.objects.filter(category=category)
    context = {'cat': category, 'boards': category_boards}
    return render(request, 'boards/board-category.html', context)


@login_required
def topic_category(request, slug, pk):
    category = get_object_or_404(Category, slug=slug, pk=pk)
    category_topics = Topic.objects.select_related().filter(board__category=category). \
        annotate(replies=Count('posts') - 1).order_by('-date_created')
    context = {'topics': category_topics}
    return render(request, 'boards/topic-category.html', context)


@login_required
def reply_topic(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()
            url = f'/t/{topic.slug}/{topic.pk}/#p-{post.id}'
            return redirect(url)
    else:
        form = PostForm()
    context = {'form': form, 'topic': topic}
    return render(request, 'boards/reply_topic.html', context)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'boards/edit_post.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_at = timezone.now()
        post.updated_by = self.request.user
        post.save()
        url = f'/t/{post.topic.slug}/{post.topic.pk}/#p-{post.id}'
        return redirect(url)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.info(request, 'Post Deleted!')
    return redirect('frilium:boards:topic_post', slug=post.topic.slug, pk=post.topic.pk)


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
    return render(request, 'boards/edit_topic.html', context)


@login_required
def show_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    url = f'{reverse("frilium:boards:topic_post", args=[post.topic.slug, post.topic.pk])}'
    return redirect(url)


@login_required
def show_topic(request, slug, pk):
    topic = get_object_or_404(Topic, slug=slug, pk=pk)
    url = f'{reverse("frilium:boards:topic_post", args=[topic.slug, topic.pk])}'
    return redirect(url)


def all_topics(request):
    context = {'topics': Topic.objects.select_related().order_by('-date_created').annotate(replies=Count('posts') - 1)}
    return render(request, 'boards/all_topics.html', context)
