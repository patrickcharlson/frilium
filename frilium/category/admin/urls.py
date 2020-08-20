from django.urls import path

from .views import list_category, create_category, edit_category, delete_category

app_name = 'category'
urlpatterns = [
    path('categories/', list_category, name='category-list'),
    path('categories/new/', create_category, name='new-category'),
    path('categories/<int:pk>/delete/', delete_category, name='category-delete'),
    path('categories/<int:pk>/edit/', edit_category, name='category-edit')
]
