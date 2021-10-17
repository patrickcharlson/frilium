from django.urls import path

from . import views

app_name = 'private'
urlpatterns = [
    path('topics/private/', views.index, name='index'),
    path('topics/private/new/', views.add_private_topic, name='new-topic-private'),
    path('topics/private/<slug:slug>/<int:topic_id>/', views.view_topic, name='view'),
    path('remove/<int:pk>/', views.remove_participant, name='remove-participant'),
    path('invite/<int:topic_id>/', views.add_participant, name='invite-participant'),
]
