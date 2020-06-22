from django.urls import path

from .views import UserProfileDetailView, ProfileTemplateView, all_user_posts

app_name = 'users'
urlpatterns = [
    path('user/options/', ProfileTemplateView.as_view(), name='user_options'),
    path('u/<str:username>/', UserProfileDetailView.as_view(), name='user_profile'),
    path('u/<str:username>/<int:pk>/posts/', all_user_posts, name='user_posts')

]
