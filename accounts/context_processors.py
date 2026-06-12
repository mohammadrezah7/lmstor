from students.models import Student
from professors.models import Professor


def user_role_info(request):
    """Add role-specific info to all templates"""
    context = {
        'user_role': request.session.get('role', None),
        'user_student': None,
        'user_professor': None,
    }
    
    if request.user.is_authenticated:
        role = request.session.get('role', None)
        if role == 'student':
            student_id = request.session.get('student_id')
            if student_id:
                try:
                    context['user_student'] = Student.objects.get(studentid=student_id)
                except Student.DoesNotExist:
                    pass
        elif role == 'professor':
            professor_id = request.session.get('professor_id')
            if professor_id:
                try:
                    context['user_professor'] = Professor.objects.get(professorid=professor_id)
                except Professor.DoesNotExist:
                    pass
    
    return context