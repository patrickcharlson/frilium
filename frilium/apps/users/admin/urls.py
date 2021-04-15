from django.urls import path

from ...users.admin.views import create_user, delete_user, edit_user, list_users

app_name = 'users'
urlpatterns = [
    path('manage-users', list_users, name='users-list'),
    path('<int:pk>/edit/', edit_user, name='edit'),
    path('add-users', create_user, name='new-users'),
    path('u/<int:pk>/delete/', delete_user, name='users-delete')
]
