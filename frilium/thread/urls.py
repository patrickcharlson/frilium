from django.urls import path, include

from .views import all_topics, list_topics, add_topic, reply_topic, show_topic, edit_topic

app_name = 'thread'
urlpatterns = [
    path('topics/', all_topics, name='topics'),
    path('b/<slug:slug>/', list_topics, name='board_topics'),
    path('<slug:slug>/t/new/', add_topic, name='new_topic'),
    path('t/<slug:slug>/edit/', edit_topic, name='edit_topic'),
    path('t/<slug:slug>/post/new/', reply_topic, name='reply_topic'),
    path('t/<slug:slug>/<int:pk>/', show_topic, name='topic'),

    path('', include('frilium.thread.private.urls'))
]
