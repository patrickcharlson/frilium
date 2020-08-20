from django.shortcuts import render

from .models import Board
from ..category.models import Category


def index(request):
    context = {'boards': Board.objects.all(),
               'categories': Category.objects.all()}
    return render(request, 'frilium/home.html', context)
