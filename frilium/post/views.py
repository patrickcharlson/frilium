from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import UpdateView

from .forms import PostForm
from .models import Post
from ..thread.models import Topic


@login_required
def list_posts(request, slug, pk):
    topic = get_object_or_404(Topic, slug=slug, pk=pk)
    topic_posts = topic.posts.select_related().order_by('created_at')
    session_key = f'viewed_topic_{topic.slug}'
    if not request.session.get(session_key, False):
        topic.views = F('views') + 1
        topic.save()
        request.session[session_key] = True
    context = {'posts': topic_posts, 'topic': topic}
    return render(request, 'frilium/post/topic_posts.html', context)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'frilium/post/edit_post.html'
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
    return redirect('frilium:post:topic_post', slug=post.topic.slug, pk=post.topic.pk)


@login_required
def show_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    url = f'{reverse("frilium:post:topic_post", args=[post.topic.slug, post.topic.pk])}'
    return redirect(url)
