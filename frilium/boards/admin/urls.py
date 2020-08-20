from django.urls import path

from .views import create_board, list_boards, \
    delete_board, edit_board, list_reports, delete_report

app_name = 'boards'
urlpatterns = [

    path('reports/', list_reports, name='reports'),
    path('reports/<int:pk>/delete/', delete_report, name='report-delete'),

    path('categories/<int:pk>/boards/', list_boards, name='boards-list'),
    path('categories/<int:pk>/board/new/', create_board, name='board-create'),

    path('categories/board/<int:pk>/delete/', delete_board, name='board-delete'),
    path('categories/board/<int:pk>/edit/', edit_board, name='board-edit')
]
