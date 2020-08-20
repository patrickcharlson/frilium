from django.urls import path, include

from .views import delete_post, show_post, PostUpdateView, list_posts

app_name = 'post'
urlpatterns = [
    path('t/<slug:slug>/<int:pk>/', list_posts, name='topic_post'),

    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('post/<slug:slug>/delete/', delete_post, name='delete_post'),
    path('post/<slug:slug>/', show_post, name='post'),

    path('', include('frilium.post.report.urls'))
]
