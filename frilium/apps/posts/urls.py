from django.urls import include, path

from .views import PostUpdateView, delete_post, show_post

app_name = 'posts'
urlpatterns = [
    path('posts/<slug:slug>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('posts/<slug:slug>/delete/', delete_post, name='delete_post'),
    path('posts/<slug:slug>/', show_post, name='posts'),

    path('likes/', include(('frilium.apps.posts.likes.urls', 'likes'), namespace='likes'))
]
