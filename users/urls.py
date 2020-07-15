from django.urls import path

from .views import UserPosts, UserTopics, password_change, email_change

app_name = 'users'
urlpatterns = [
    path('options/email-change/', email_change, name='email-change'),
    path('options/password-change/', password_change, name='password-change'),
    path('u/<str:username>/<int:pk>/posts/', UserPosts.as_view(), name='user_posts'),
    path('u/<str:username>/<int:pk>/topics/', UserTopics.as_view(), name='user_topics'),
]
