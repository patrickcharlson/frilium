from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ReportForm
from ..models import Post


def create_report(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.post = post
            report.reported_by = request.user
            report.save()
            messages.info(request, 'Your report has been sent for review')
            url = f'{reverse("frilium:posts:topic_post", args=[post.topic.slug, post.topic.pk])}'
            return redirect(url)
    else:
        form = ReportForm()
    context = {'form': form, 'posts': post}
    return render(request, 'frilium/posts/report/create_report.html', context)
