from django.urls import path

from .views import UserPosts, UserTopics, password_change, email_change, update, user_details

app_name = 'users'
urlpatterns = [
    path('options/email-change/', email_change, name='email-change'),
    path('options/password-change/', password_change, name='password-change'),
    path('options/edit-details/', update, name='edit-user'),
    path('u/<str:username>/<int:pk>/posts/', UserPosts.as_view(), name='user_posts'),
    path('u/<str:username>/<int:pk>/topics/', UserTopics.as_view(), name='user_topics'),
    path('u/<str:username>/<int:pk>/details/', user_details, name='user-details')
]
