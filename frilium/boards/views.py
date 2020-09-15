from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Board
from ..category.models import Category


@login_required
def index(request):
    context = {'boards': Board.objects.all(),
               'categories': Category.objects.all()}
    return render(request, 'frilium/home.html', context)
