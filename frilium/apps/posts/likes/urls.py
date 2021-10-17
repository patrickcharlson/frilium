from django.urls import path

from . import views

urlpatterns = [
    path("<int:content_type_id>/<str:object_id>/", views.json_set_like, name="json_set_like")
]
