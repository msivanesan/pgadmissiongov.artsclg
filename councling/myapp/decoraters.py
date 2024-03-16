from django.http import  HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from functools import wraps

def group_required(group_names):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url="login")
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in.")
            if request.user.role!=group_names[0]:
                return HttpResponseForbidden("<h1>You do not have permission to view this page.</h1>")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


