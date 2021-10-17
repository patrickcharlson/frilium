from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddCategoryForm, EditCategoryForm
from ..models import Category
from ...core.utils.decorators import administrator_required


@administrator_required
def list_category(request):
    context = {'categories': Category.objects.filter(parent=None, is_private=False)}
    return render(request, 'frilium/admin/categories/category_list.html', context)


@administrator_required()
def create_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'A new categories has been added!')
            return redirect('frilium:admin:categories:categories-list')
    else:
        form = AddCategoryForm()
    context = {'form': form}
    return render(request, 'frilium/admin/categories/new_category.html', context)


@administrator_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = EditCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.info(request, 'Category has been updated!')
            return redirect('frilium:admin:categories:category-edit', category.pk)
    else:
        form = EditCategoryForm(instance=category)
    context = {'form': form, 'c': category}
    return render(request, 'frilium/admin/categories/edit_category.html', context)


@administrator_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.info(request, 'Category deleted!')
    return redirect('frilium:admin:categories:categories-list')
