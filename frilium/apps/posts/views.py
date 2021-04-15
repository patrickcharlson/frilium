from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import UpdateView

from .forms import PostForm
from .models import Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'frilium/posts/edit_post.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'posts'
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
        return queryset.filter(user=self.request.user)


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.info(request, 'Post Deleted!')
    return redirect('frilium:topics:view', slug=post.topic.slug, pk=post.topic.pk)


@login_required
def show_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    url = f'{reverse("frilium:topics:view", args=[post.topic.slug, post.topic.pk])}'
    return redirect(url)
