from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect

from frilium.core.utils.decorators import administrator_required
from frilium.user.admin.forms import UserForm, NewUserForm

User = get_user_model()


@administrator_required
def user_list(request):
    context = {'users': User.objects.all().order_by('-date_joined', '-pk')}
    return render(request, 'frilium/admin/userlist.html', context)


@administrator_required
def edit(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.info(request, 'This profile has been updated')
            return redirect('frilium:admin:user:edit', user.pk)
    else:
        form = UserForm(instance=user)
        context = {'form': form, 'user': user}
        return render(request, 'frilium/admin/edit.html', context)


@administrator_required
def create_user(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['new_password']
            )
            messages.success(request, f'New user {new_user.username} has been registered')
            return redirect('frilium:admin:user:edit', new_user.pk)
    else:
        form = NewUserForm()
    context = {'form': form}
    return render(request, 'frilium/admin/new_user.html', context)
