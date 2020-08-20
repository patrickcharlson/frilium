from django.urls import path

from .views import create_report

app_name = 'report'
urlpatterns = [
    path('post/report/<int:pk>/create/', create_report, name='report'),
]
