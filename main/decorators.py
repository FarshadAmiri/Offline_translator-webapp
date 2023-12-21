from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def admins_only(view_func):
    @login_required(login_url='users:login')
    def wrapper(request, *args, **kwargs):
        if (request.user.groups.filter(name='Admins').exists()) or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('users:login')  # Redirect to login page or any other page
    return wrapper