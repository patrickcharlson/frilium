from django.urls import path, include

from .views import dashboard

app_name = 'admin'
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('users/', include('frilium.user.admin.urls')),
    path('', include('frilium.boards.admin.urls')),
    path('', include('frilium.category.admin.urls')),
]
