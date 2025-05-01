from django.http import HttpResponseForbidden
from django.urls import resolve

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip middleware for auth endpoints
        if request.path.startswith('/api/auth/') or request.path.startswith('/admin/'):
            return self.get_response(request)
            
        # Get the current view and its required permissions
        try:
            resolver_match = resolve(request.path_info)
            view = resolver_match.func
            required_permission = getattr(view, 'required_permission', None)
            
            if required_permission:
                if not request.user.role or required_permission not in request.user.role.permissions:
                    return HttpResponseForbidden("Insufficient permissions")
                    
        except:
            pass
            
        return self.get_response(request)