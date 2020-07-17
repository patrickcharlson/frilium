from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, UpdateView

from .forms import NewTopicForm, PostForm, EditTopicForm, EditPostForm
from .models import Board, Post, Topic, Category

User = get_user_model()


# class BoardsListView(ListView):
#     model = Board
#     context_object_name = 'boards'
#     template_name = 'home.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.select_related().all()
#         return context
#
#
# index = BoardsListView.as_view()


def index(request):
    context = {'boards': Board.objects.all(),
               'categories': Category.objects.all()}
    return render(request, 'home.html', context)


class TopicsListView(LoginRequiredMixin, ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/topics.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs.get('slug'))
        queryset = self.board.topics.select_related() \
            .order_by('-date_created').annotate(replies=Count('posts') - 1)
        return queryset


class NewTopicView(LoginRequiredMixin, View):

    def render(self, request, slug):
        board = get_object_or_404(Board, slug=slug)
        return render(request, 'boards/new_topic.html', {'board': board, 'form': self.form})

    def post(self, request, slug):
        board = get_object_or_404(Board, slug=slug)
        self.form = NewTopicForm(request.POST)
        if self.form.is_valid():
            topic = self.form.save(commit=False)
            topic.board = board
            topic.created_by = request.user
            topic.save()
            Post.objects.create(
                message=self.form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('boards:topic_post', slug=topic.slug, pk=topic.pk)
        return self.render(request, slug)

    def get(self, request, slug):
        self.form = NewTopicForm()
        return self.render(request, slug)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/topic_posts.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        session_key = f'viewed_topic_{self.topic.slug}'
        if not self.request.session.get(session_key, False):
            self.topic.views = F('views') + 1
            self.topic.save()
            self.request.session[session_key] = True
        context = super().get_context_data(**kwargs)
        context['topic'] = self.topic
        return context

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, slug=self.kwargs.get('slug'), pk=self.kwargs.get('pk'))
        queryset = self.topic.posts.select_related('created_by', 'topic', 'updated_by').order_by('created_at')
        return queryset


class BoardCategoryListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/board-category.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['cat'] = self.category
        return context

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        queryset = Board.objects.filter(category=self.category)
        return queryset


class NewPostView(LoginRequiredMixin, View):

    def render(self, request, slug):
        topic = get_object_or_404(Topic, slug=slug)
        return render(request, 'boards/reply_topic.html', {'topic': topic, 'form': self.form})

    def post(self, request, slug):
        topic = get_object_or_404(Topic, slug=slug)
        self.form = PostForm(request.POST)
        if self.form.is_valid():
            post = self.form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()
            url = f'/t/{topic.slug}/{topic.pk}/#p-{post.id}'
            return redirect(url)
        return self.render(request, slug)

    def get(self, request, slug):
        self.form = PostForm()
        return self.render(request, slug)


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


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.info(request, 'Post Deleted!')
    return redirect('boards:topic_post', slug=post.topic.slug, pk=post.topic.pk)


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
    url = f'{reverse("boards:topic_post", args=[post.topic.slug, post.topic.pk])}'
    return redirect(url)


@login_required
def show_topic(request, slug, pk):
    topic = get_object_or_404(Topic, slug=slug, pk=pk)
    url = f'{reverse("boards:topic_post", args=[topic.slug, topic.pk])}'
    return redirect(url)


def all_topics(request):
    context = {'topics': Topic.objects.select_related().order_by('-date_created').annotate(replies=Count('posts') - 1)}
    return render(request, 'boards/all_topics.html', context)
