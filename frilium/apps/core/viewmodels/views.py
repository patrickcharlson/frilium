from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from ...categories.models import Category
from ...posts.forms import PostForm
from ...posts.models import Post
from ...topics.models import Topic


class BaseViewForm(FormView):
    category_pk_url_kwarg = None
    post_pk_url_kwarg = None
    topic_pk_url_kwarg = None
    post_form_class = PostForm

    def get(self, request, *args, **kwargs):
        post_form_class = self.get_post_form_class()
        post_form = self.get_post_form(post_form_class)

        return self.response_class(
            self.get_context_data(post_form=post_form)
        )

    def post(self, request, *args, **kwargs):
        post_form_class = self.get_post_form_class()
        post_form = self.get_post_form(post_form_class)

        if post_form.is_valid():
            return self.form_valid(post_form)
        else:
            return self.form_invalid(post_form)

    def get_post_form(self, form_class):
        return form_class(**self.get_post_form_kwargs())

    def get_post_form_class(self):
        return self.post_form_class

    def get_post_form_kwargs(self):
        kwargs = {
            'user': self.request.user,
            'category': self.get_category(),
            'topic': self.get_topic(),
        }
        post = self.get_post()
        if post:
            kwargs.update({'instance': post})

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST
            })

        return kwargs

    def get_context_data(self, **kwargs):
        context = kwargs
        if 'view' not in context:
            context['view'] = self

        context['category'] = self.get_category()
        context['topic'] = self.get_topic()
        context['post'] = self.get_post()

        return context

    def get_category(self):
        pk = self.kwargs.get(self.category_pk_url_kwarg, None)
        if not pk:
            return
        if not hasattr(self, '_category'):
            self._category = get_object_or_404(Category, pk=pk)  # noqa

        return self._category

    def get_topic(self):
        pk = self.kwargs.get(self.topic_pk_url_kwarg, None)
        if not pk:
            return
        if not hasattr(self, '_topic'):
            self._topic = get_object_or_404(Topic, pk=pk)  # noqa

        return self._topic

    def get_post(self):
        pk = self.kwargs.get(self.post_pk_url_kwarg, None)
        if not pk:
            return
        if not hasattr(self, '_post'):
            self._post = get_object_or_404(Post, pk=pk)  # noqa

        return self._post

    def form_valid(self, post_form, **kwargs):
        self.category_post = post_form.save()  # noqa

        return HttpResponseRedirect(self.get_success_url())


class PostFormView(SingleObjectMixin, BaseViewForm):
    category_pk_url_kwarg = 'category_pk'
    post_pk_url_kwarg = 'pk'
    topic_pk_url_kwarg = 'topic_pk'
