from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def dti_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('index')  # Substitua 'index' pelo nome da URL da página inicial
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def colaborador_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('inicio')  # Substitua 'inicio' pelo nome da URL da página inicial
        return view_func(request, *args, **kwargs)
    return _wrapped_view

