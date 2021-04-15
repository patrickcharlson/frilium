from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('u/<str:username>/', views.user_profile, name='profile'),
    path('u/<str:username>/edit/email/', views.email_change, name='email-change'),
    path('u/<str:username>/edit/password/', views.password_change, name='password-change'),
    path('u/<str:username>/edit/preference', views.update, name='edit-users'),
    path('u/<str:username>/posts/', views.user_posts, name='user_posts'),
    path('u/<str:username>/topics/', views.user_topics, name='user_topics'),
]
