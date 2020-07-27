from django.urls import path, include

app_name = 'frilium'
urlpatterns = [
    path('admincp/', include('frilium.admin.urls')),
    path('auth/', include('frilium.auth.urls')),
    path('', include('frilium.boards.urls')),
    path('', include('frilium.user.urls')),
]
