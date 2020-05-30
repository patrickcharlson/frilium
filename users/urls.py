from django.urls import path

from .views import UserProfileDetailView

app_name = 'users'
urlpatterns = [
    path('user/<str:username>/', UserProfileDetailView.as_view(), name='user_profile')
]
