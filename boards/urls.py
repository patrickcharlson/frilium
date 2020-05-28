from django.urls import path

from .views import BoardsListView, new_topic, reply_topic, PostUpdateView, TopicsListView, PostListView, users_list

app_name = 'boards'
urlpatterns = [
    path('', BoardsListView.as_view(), name='home'),
    path('members/', users_list, name='users'),
    path('boards/<slug:slug>/', TopicsListView.as_view(), name='board_topics'),
    path('<slug:slug>/topic/new/', new_topic, name='new_topic'),
    path('topic/<slug:slug>/', PostListView.as_view(), name='topic_post'),
    path('topic/<slug:slug>/post/new/', reply_topic, name='reply_topic'),
    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='edit_post')
]
