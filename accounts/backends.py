from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User, Group, Permission
from students.models import Student
from professors.models import Professor


class MultiRoleAuthBackend(BaseBackend):
    """
    Custom authentication backend:
    - For Students: NationalID = username, Email = password
    - For Professors: Email = username, Email = password
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        role = None
        
        # Try Student authentication (NationalID)
        try:
            student = Student.objects.get(nationalid=username)
            if student.email and student.email == password:
                # Create or get Django User for this student
                user, created = User.objects.get_or_create(
                    username=student.nationalid,
                    defaults={
                        'email': student.email,
                        'first_name': student.firstname,
                        'last_name': student.lastname,
                    }
                )
                if created:
                    user.set_unusable_password()
                    user.save()
                    # Assign to Students group
                    student_group, _ = Group.objects.get_or_create(name='Students')
                    user.groups.add(student_group)
                
                role = 'student'
                # Store extra info in session
                request.session['role'] = 'student'
                request.session['student_id'] = student.studentid
        except Student.DoesNotExist:
            pass
        
        # Try Professor authentication (Email)
        if user is None:
            try:
                professor = Professor.objects.get(email=username)
                if professor.email == password:
                    user, created = User.objects.get_or_create(
                        username=professor.email,
                        defaults={
                            'email': professor.email,
                            'first_name': professor.firstname,
                            'last_name': professor.lastname,
                        }
                    )
                    if created:
                        user.set_unusable_password()
                        user.save()
                        professor_group, _ = Group.objects.get_or_create(name='Professors')
                        user.groups.add(professor_group)
                    
                    role = 'professor'
                    request.session['role'] = 'professor'
                    request.session['professor_id'] = professor.professorid
            except Professor.DoesNotExist:
                pass
        
        # If still not authenticated, try Django superuser
        if user is None:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password) or user.is_superuser:
                    # Admin login
                    request.session['role'] = 'admin'
                    role = 'admin'
                else:
                    return None
            except User.DoesNotExist:
                return None
        
        return user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def get_group_permissions(self, user_obj, obj=None):
        return Permission.objects.filter(group__user=user_obj)
    
    def get_all_permissions(self, user_obj, obj=None):
        return Permission.objects.filter(group__user=user_obj)
    
    def has_perm(self, user_obj, perm, obj=None):
        return Permission.objects.filter(group__user=user_obj, codename=perm.split('.')[-1]).exists()
    
    def has_module_perms(self, user_obj, app_label):
        return user_obj.is_superuser or Permission.objects.filter(
            group__user=user_obj,
            content_type__app_label=app_label
        ).exists()