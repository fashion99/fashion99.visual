from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def feature_required(feature):
    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if not request.user.has_feature_permission(feature):
                raise PermissionDenied
            return view(request, *args, **kwargs)
        return wrapped
    return decorator