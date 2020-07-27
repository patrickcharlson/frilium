from django.urls import path

from .views import PostUpdateView, delete_post, edit_topic, \
    show_post, show_topic, index, \
    all_topics, topic_category, post_list, board_category, topics_list, add_topic, reply_topic

app_name = 'boards'
urlpatterns = [
    # Boards
    path('', index, name='home'),

    path('topics/', all_topics, name='topics'),
    path('b/<slug:slug>/', topics_list, name='board_topics'),
    path('<slug:slug>/t/new/', add_topic, name='new_topic'),
    path('t/<slug:slug>/<int:pk>/', post_list, name='topic_post'),
    path('t/<slug:slug>/edit/', edit_topic, name='edit_topic'),
    path('t/<slug:slug>/post/new/', reply_topic, name='reply_topic'),
    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('post/<slug:slug>/delete/', delete_post, name='delete_post'),
    path('post/<slug:slug>/', show_post, name='post'),
    path('t/<slug:slug>/<int:pk>/', show_topic, name='topic'),
    path('c/b/<slug:slug>/<int:pk>/', board_category, name='cat-list'),
    path('c/t/<slug:slug>/<int:pk>/', topic_category, name='topic-category')
]
