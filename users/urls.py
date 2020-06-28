from django.urls import path

from .views import UserProfileDetailView, ProfileTemplateView, UserPosts, UserTopics

app_name = 'users'
urlpatterns = [
    path('user/options/', ProfileTemplateView.as_view(), name='user_options'),
    path('u/<str:username>/', UserProfileDetailView.as_view(), name='user_profile'),
    path('u/<str:username>/<int:pk>/posts/', UserPosts.as_view(), name='user_posts'),
    path('u/<str:username>/<int:pk>/topics/', UserTopics.as_view(), name='user_topics')
]
