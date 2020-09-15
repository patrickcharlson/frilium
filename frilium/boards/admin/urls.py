from django.urls import path

from .views import create_board, list_boards, delete_board, edit_board

app_name = 'boards'
urlpatterns = [

    path('categories/<int:pk>/boards/', list_boards, name='boards-list'),
    path('categories/<int:pk>/board/new/', create_board, name='board-create'),
    path('categories/board/<int:pk>/delete/', delete_board, name='board-delete'),
    path('categories/board/<int:pk>/edit/', edit_board, name='board-edit')
]
