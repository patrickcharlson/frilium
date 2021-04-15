from django.urls import include, path

from .views.index import dashboard

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('users/', include('frilium.apps.users.admin.urls')),
    path('', include('frilium.apps.categories.admin.urls')),
]
