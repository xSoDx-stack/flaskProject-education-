from flask_rbac import RBAC


class MRBAC(RBAC):
    def exempt(self, endpoint=None):
        def decorator(view_func):
            self.acl.exempt(endpoint or view_func.__name__)
            return view_func

        return decorator
