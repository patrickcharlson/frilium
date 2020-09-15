from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import TopicPrivateForm, TopicPrivateManyForm, PrivateTopicInviteForm
from .models import TopicPrivate
from ..models import Topic
from ...core.utils.views import post_data
from ...post.forms import PostForm
from ...post.models import Post

User = get_user_model()


@login_required
def index(request):
    topics = Topic.objects.filter(private_topics__user=request.user).order_by(
        '-date_created').annotate(replies=Count('posts') - 1)
    return render(request, 'frilium/thread/private/index.html', {'topics': topics})


@login_required
def new_private_topic(request):
    user = request.user
    if request.method == 'POST':
        t_form = TopicPrivateForm(request.POST, user=user)
        p_form = PostForm(request.POST, user=user)
        tp_form = TopicPrivateManyForm(request.POST, user=user)

        if all([t_form.is_valid(), p_form.is_valid(), tp_form.is_valid()]):
            topic = t_form.save()
            p_form.topic = topic
            p_form.save()
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


@login_required
def list_private_posts(request, slug, topic_id):
    private_topic = get_object_or_404(TopicPrivate, topic_id=topic_id, user=request.user)
    topic = private_topic.topic
    if topic.slug != slug:
        return HttpResponsePermanentRedirect(topic.get_absolute_url())

    session_key = f'viewed_topic_{topic.pk}'
    if not request.session.get(session_key, None):
        topic.views = F('views') + 1
        topic.save()
        request.session[session_key] = True
    posts = Post.objects.filter(topic=topic).order_by('created_at')
    participants = TopicPrivate.objects.filter(topic=topic).order_by('-is_owner')
    context = {'topic': topic,
               'posts': posts,
               'private_topic': private_topic,
               'participants': participants
               }
    return render(request, 'frilium/thread/private/private_posts.html', context)


@login_required
def remove_participant(request, pk):
    private_topic = TopicPrivate.objects.for_delete_or_404(pk, request.user)
    thread_owner = False
    remaining_participants = []
    topic = private_topic.topic
    participants = TopicPrivate.objects.filter(topic=topic)

    for participant in participants:
        if participant.user_id == topic.user_id:
            thread_owner = participant.is_owner
        else:
            remaining_participants.append(participant.user)

    if not remaining_participants:
        topic.delete()
    else:
        topic.private_topics.filter(user_id=private_topic.user_id).delete()
        if thread_owner:
            topic.delete()
    if request.user.pk == private_topic.user_id:
        return redirect(reverse("frilium:thread:private:index"))

    return redirect(private_topic.get_absolute_url())


@login_required
def add_participant(request, topic_id):
    private_topic = TopicPrivate.objects.create_or_404(topic_id, request.user)
    form = PrivateTopicInviteForm(topic=private_topic.topic, data=post_data(request))
    if form.is_valid():
        form.save()
    return redirect(private_topic.get_absolute_url())
