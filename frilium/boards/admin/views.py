from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from ...boards.admin.forms import AddBoardForm, EditBoardForm
from ...boards.models import Category, Board
from ...core.utils.decorators import administrator_required
from ...post.report.models import Report


@administrator_required
def create_board(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = AddBoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.category = category
            board.save()
            messages.success(request, 'Added a new Board')
            return redirect('frilium:admin:boards:boards-list', category.pk)
    else:
        form = AddBoardForm()
    context = {'form': form, 'category': category}
    return render(request, 'frilium/admin/boards/create_board.html', context)


@administrator_required
def list_boards(request, pk):
    category = get_object_or_404(Category, pk=pk)
    boards = Board.objects.filter(category=category)
    context = {'boards': boards, 'category': category}
    return render(request, 'frilium/admin/boards/list_boards.html', context)


@administrator_required
def edit_board(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = EditBoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            messages.info(request, 'This board has been updated!')
            return redirect('frilium:admin:boards:board-edit', board.pk)
    else:
        form = EditBoardForm(instance=board)
    context = {'form': form}
    return render(request, 'frilium/admin/boards/edit_board.html', context)


@administrator_required
def delete_board(request, pk):
    board = get_object_or_404(Board, pk=pk)
    board.delete()
    messages.info(request, 'A board has been deleted!')
    return redirect('frilium:admin:boards:boards-list', board.category.pk)


@administrator_required
def list_reports(request):
    context = {'reports': Report.objects.all()}
    return render(request, 'frilium/admin/list_reports.html', context)


def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.delete()
    messages.info(request, 'Report deleted!')
    return redirect('frilium:admin:boards:reports')
