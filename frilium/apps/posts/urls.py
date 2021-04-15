from django.urls import path, include

from .views import delete_post, show_post, PostUpdateView

app_name = 'posts'
urlpatterns = [
    path('posts/<slug:slug>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('posts/<slug:slug>/delete/', delete_post, name='delete_post'),
    path('posts/<slug:slug>/', show_post, name='posts'),

    path('', include('frilium.apps.posts.report.urls'))
]
