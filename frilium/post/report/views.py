from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from frilium.post.models import Post
from frilium.post.report.forms import ReportForm


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
            url = f'{reverse("frilium:post:topic_post", args=[post.topic.slug, post.topic.pk])}'
            return redirect(url)
    else:
        form = ReportForm()
    context = {'form': form, 'post': post}
    return render(request, 'frilium/post/report/create_report.html', context)
