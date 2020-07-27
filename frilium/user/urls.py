from django.urls import path

from .views import password_change, email_change, update, user_details, user_posts, user_topics

app_name = 'user'
urlpatterns = [
    path('options/email-change/', email_change, name='email-change'),
    path('options/password-change/', password_change, name='password-change'),
    path('options/edit-details/', update, name='edit-user'),
    path('u/<str:username>/<int:pk>/posts/', user_posts, name='user_posts'),
    path('u/<str:username>/<int:pk>/topics/', user_topics, name='user_topics'),
    path('u/<str:username>/<int:pk>/details/', user_details, name='user-details')
]
