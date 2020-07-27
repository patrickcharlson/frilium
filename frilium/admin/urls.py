from django.urls import path, include

from frilium.admin.views import dashboard

app_name = 'admin'
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('users/', include('frilium.user.admin.urls'))
]
