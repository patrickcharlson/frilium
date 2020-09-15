from django.urls import path, include

from . import views

app_name = 'thread'
urlpatterns = [
    path('topics/', views.all_topics, name='topics'),
    path('topics/my/', views.my_topics, name='my-topics'),
    path('b/<slug:slug>/my/', views.my_topics, name='my-topics'),
    path('b/<slug:slug>/', views.list_topics, name='board_topics'),
    path('<slug:slug>/t/new/', views.add_topic, name='new_topic'),
    path('t/<slug:slug>/edit/', views.edit_topic, name='edit_topic'),
    path('t/<slug:slug>/post/new/', views.reply_topic, name='reply_topic'),
    path('t/<slug:slug>/<int:pk>/', views.show_topic, name='topic'),

    path('', include('frilium.thread.private.urls'))
]
