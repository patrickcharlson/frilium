from django.urls import path

from .views import BoardsListView, PostUpdateView, TopicsListView, PostListView, UsersListView, \
    NewPostView, NewTopicView, delete_post, edit_topic

app_name = 'boards'
urlpatterns = [
    path('', BoardsListView.as_view(), name='home'),
    path('members/', UsersListView.as_view(), name='users'),
    path('boards/<slug:slug>/', TopicsListView.as_view(), name='board_topics'),
    path('<slug:slug>/topic/new/', NewTopicView.as_view(), name='new_topic'),
    path('topic/<slug:slug>/', PostListView.as_view(), name='topic_post'),
    path('topic/<slug:slug>/edit/', edit_topic, name='edit_topic'),
    path('topic/<slug:slug>/post/new/', NewPostView.as_view(), name='reply_topic'),
    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('post/<slug:slug>/delete/', delete_post, name='delete_post')
]
