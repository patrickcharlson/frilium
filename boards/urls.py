from django.urls import path

from .views import PostUpdateView, TopicsListView, PostListView, UsersListView, \
    NewPostView, NewTopicView, delete_post, edit_topic, show_post, show_topic, index, BoardCategoryListView

app_name = 'boards'
urlpatterns = [
    # Boards
    path('', index, name='home'),

    # Users
    path('users/', UsersListView.as_view(), name='users'),

    path('b/<slug:slug>/', TopicsListView.as_view(), name='board_topics'),
    path('<slug:slug>/t/new/', NewTopicView.as_view(), name='new_topic'),
    path('t/<slug:slug>/<int:pk>/', PostListView.as_view(), name='topic_post'),
    path('t/<slug:slug>/edit/', edit_topic, name='edit_topic'),
    path('t/<slug:slug>/post/new/', NewPostView.as_view(), name='reply_topic'),
    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('post/<slug:slug>/delete/', delete_post, name='delete_post'),
    path('post/<slug:slug>/', show_post, name='post'),
    path('t/<slug:slug>/<int:pk>/', show_topic, name='topic'),
    path('c/<slug:slug>/<int:pk>/', BoardCategoryListView.as_view(), name='cat-list')
]
