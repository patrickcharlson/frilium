from django.urls import path

from .views import BoardsListView, board_topics, new_topic, topic_posts

app_name = 'boards'
urlpatterns = [
    path('', BoardsListView.as_view(), name='home'),
    path('boards/<slug:slug>/', board_topics, name='board_topics'),
    path('<slug:slug>/topic/new/', new_topic, name='new_topic'),
    path('topic/<slug:slug>/', topic_posts, name='topic_post')
]
