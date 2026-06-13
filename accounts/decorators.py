from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def role_required(allowed_roles):
    """
    Decorator to restrict access based on user role.
    Usage: @role_required(['admin', 'professor'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_role = request.session.get('role', None)
            
            if not request.user.is_authenticated:
                messages.error(request, 'لطفاً ابتدا وارد شوید.')
                return redirect('accounts:login')
            
            if user_role not in allowed_roles:
                messages.error(request, '⛔ شما دسترسی به این بخش را ندارید!')
                # Redirect based on role
                if user_role == 'student':
                    return redirect('students:my_dashboard')
                elif user_role == 'professor':
                    return redirect('professors:my_dashboard')
                else:
                    return redirect('core:dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_only(view_func):
    """Only admin can access"""
    return role_required(['admin'])(view_func)


def student_only(view_func):
    """Only students can access"""
    return role_required(['student'])(view_func)


def professor_only(view_func):
    """Only professors can access"""
    return role_required(['professor'])(view_func)


def admin_or_professor(view_func):
    """Admin and professors can access"""
    return role_required(['admin', 'professor'])(view_func)