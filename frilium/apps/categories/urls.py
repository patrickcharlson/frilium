from django.urls import path

from . import views

app_name = 'categories'
urlpatterns = [
    path('categories/', views.list_categories, name='categories'),
    path('c/<slug:slug>/<int:pk>/', views.view_category, name='view'),
]
