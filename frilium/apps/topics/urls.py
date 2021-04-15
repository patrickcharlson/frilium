from django.urls import path, include

from . import views

app_name = 'topics'
urlpatterns = [
    path('t/<slug:slug>/<int:pk>/', views.view_topic, name='view'),
    path('<int:pk>/t/new/', views.add_topic, name='new_topic'),
    path('t/<slug:slug>/edit/', views.edit_topic, name='edit_topic'),
    path('t/<slug:slug>/posts/new/', views.reply_topic, name='reply_topic'),
    path('t/<slug:slug>/<int:pk>/', views.show_topic, name='topic'),

    path('', include('frilium.apps.topics.private.urls'))
]
