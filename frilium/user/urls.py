from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('options/email-change/', views.email_change, name='email-change'),
    path('options/password-change/', views.password_change, name='password-change'),
    path('options/edit-details/', views.update, name='edit-user'),
    path('u/<str:username>/<int:pk>/posts/', views.user_posts, name='user_posts'),
    path('u/<str:username>/<int:pk>/topics/', views.user_topics, name='user_topics'),
    path('u/<str:username>/<int:pk>/details/', views.user_details, name='user-details')
]
