from django.urls import path

from . import views

app_name = 'private'
urlpatterns = [
    path('topics/private/', views.index, name='index'),
    path('topics/private/new/', views.new_private_topic, name='new-topic-private'),
    path('thread/private/<slug:slug>/<int:pk>/', views.list_private_posts, name='private-posts')
]
