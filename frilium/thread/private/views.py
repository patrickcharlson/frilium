from django.contrib.auth import get_user_model
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TopicPrivateForm, TopicPrivateManyForm
from .models import TopicPrivate
from ..models import Topic
from ...post.forms import PostForm
from ...post.models import Post

User = get_user_model()


def index(request):
    topics = Topic.objects.filter(private_topics__user=request.user).order_by('-date_created')
    return render(request, 'frilium/thread/private/index.html', {'topics': topics})


def new_private_topic(request, pk=None):
    user = request.user
    if request.method == 'POST':
        t_form = TopicPrivateForm(request.POST, user=user)
        p_form = PostForm(request.POST, user=user)
        tp_form = TopicPrivateManyForm(request.POST, user=user)

        if all([t_form.is_valid(), p_form.is_valid(), tp_form.is_valid()]):
            if pk:
                user_p = get_object_or_404(User, pk=pk)
                if not user_p.update_post_hash(t_form.get_topic_hash()):
                    return redirect(request.POST.get('next', None) or t_form.board.get_absolute_url())

            topic = t_form.save(commit=False)
            topic.created_by = user
            topic.save()
            p_post = p_form.save(commit=False)
            p_post.topic = topic
            p_post.created_by = user
            p_post.save()
            tp_form.topic = topic
            tp_form.save_m2m()
            return redirect(topic.get_absolute_url())

    else:
        t_form = TopicPrivateForm(user=user)
        p_form = PostForm(user=user)
        tp_form = TopicPrivateManyForm(user=user)
    context = {'t_form': t_form,
               'p_form': p_form,
               'tp_form': tp_form
               }
    return render(request, 'frilium/thread/private/new_private_topic.html', context)


def list_private_posts(request, slug, pk):
    private_topic = get_object_or_404(TopicPrivate, pk=pk)
    topic = private_topic.topic
    if topic.slug != slug:
        return HttpResponsePermanentRedirect(topic.get_absolute_url())

    posts = Post.objects.filter(topic=topic).order_by('created_at')
    context = {'topic': topic,
               'posts': posts,
               'private_topic': private_topic
               }
    return render(request, 'frilium/thread/private/private_posts.html', context)
