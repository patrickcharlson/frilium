from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView

from .forms import NewTopicForm, PostForm
from .models import Board, Post, Topic

User = get_user_model()


class BoardsListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'
    paginate_by = 7


class TopicsListView(LoginRequiredMixin, ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/topics.html'
    paginate_by = 3
    login_url = 'account_login'

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs.get('slug'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class NewTopicView(LoginRequiredMixin, View):
    login_url = 'account_login'

    def render(self, request, slug):
        board = get_object_or_404(Board, slug=slug)
        return render(request, 'boards/new_topic.html', {'board': board, 'form': self.form})

    def post(self, request, slug):
        board = get_object_or_404(Board, slug=slug)
        self.form = NewTopicForm(request.POST)
        if self.form.is_valid():
            topic = self.form.save(commit=False)
            topic.board = board
            topic.user = request.user
            topic.save()
            Post.objects.create(
                message=self.form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('boards:topic_post', slug=topic.slug)
        return self.render(request, slug)

    def get(self, request, slug):
        self.form = NewTopicForm()
        return self.render(request, slug)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/topic_posts.html'
    paginate_by = 2
    login_url = 'account_login'

    def get_context_data(self, *, object_list=None, **kwargs):
        session_key = f'viewed_topic_{self.topic.slug}'
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        context = super().get_context_data(**kwargs)
        context['topic'] = self.topic
        return context

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, slug=self.kwargs.get('slug'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


class NewPostView(LoginRequiredMixin, View):
    login_url = 'account_login'

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
            return redirect('boards:topic_post', slug=topic.slug)
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
    login_url = 'account_login'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_at = timezone.now()
        post.updated_by = self.request.user
        post.save()
        return redirect('boards:topic_post', slug=post.topic.slug)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'boards/members.html'
    paginate_by = 5
    login_url = 'account_login'


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('boards:topic_post', slug=post.topic.slug)


class DeletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('boards:topic_post')
