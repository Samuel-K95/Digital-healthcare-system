from functools import wraps
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from .policy import get_role


def require_auth(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return JsonResponse({'error': 'authentication required'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped


def require_policy(check_func):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            allowed = check_func(request, *args, **kwargs)
            if not allowed:
                return HttpResponseForbidden('forbidden')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
