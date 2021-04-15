from django.urls import path

from .views import create_report

app_name = 'report'
urlpatterns = [
    path('posts/report/<int:pk>/create/', create_report, name='report'),
]
