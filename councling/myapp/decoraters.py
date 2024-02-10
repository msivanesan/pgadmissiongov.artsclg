from django.http import  HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from functools import wraps

def group_required(group_names):
    if isinstance(group_names, str):
        group_names = [group_names]  # Ensure group_names is always a list

    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url="login")
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in.")
            user_groups = set(request.user.groups.values_list('name', flat=True))
            if not set(group_names).intersection(user_groups):
                return HttpResponseForbidden("<h1>You do not have permission to view this page.</h1>")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


