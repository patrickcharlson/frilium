from django.urls import path

from .views import UserProfileDetailView, ProfileTemplateView

app_name = 'users'
urlpatterns = [
    path('user/options/', ProfileTemplateView.as_view(), name='user_options'),
    path('u/<str:username>/', UserProfileDetailView.as_view(), name='user_profile'),

]
