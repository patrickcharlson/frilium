from django.urls import path

from .views import index

app_name = 'boards'
urlpatterns = [
    path('', index, name='home'),
]
