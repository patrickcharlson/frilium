from django.urls import path

from . import views

app_name = 'categories'
urlpatterns = [
    path('categories/', views.list_category, name='categories-list'),
    path('categories/new/', views.create_category, name='new-category'),
    path('categories/<int:pk>/delete/', views.delete_category, name='category-delete'),
    path('categories/<int:pk>/edit/', views.edit_category, name='category-edit'),
]
