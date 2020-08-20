from django.urls import path

from .views import board_category, topic_category

app_name = 'category'
urlpatterns = [
    path('c/b/<slug:slug>/<int:pk>/', board_category, name='cat-list'),
    path('c/t/<slug:slug>/<int:pk>/', topic_category, name='topic-category'),
]
