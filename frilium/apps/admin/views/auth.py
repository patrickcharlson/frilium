from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from frilium.apps.admin import auth
from frilium.apps.users.admin.forms import AdminAuthenticationForm


@sensitive_post_parameters()
@never_cache
def login(request):
    form = AdminAuthenticationForm(request)

    if request.method == "POST":
        form = AdminAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.user_cache)
            return redirect('frilium:admin:dashboard')

    context = {"form": form}
    return render(request, 'frilium/admin/login.html', context)


@never_cache
def logout(request):
    if request.method == 'POST':
        auth.remove_admin_authorization(request)
        messages.info(request, "Your admin session has been closed")
    return redirect('frilium:admin:dashboard')
