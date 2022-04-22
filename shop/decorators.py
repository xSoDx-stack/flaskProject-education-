from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, abort


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.cant(role):
                abort(404)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return role_required('admin')(f)
