from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Professor
from courses.models import ClassSection, Enrollment
from accounts.decorators import professor_only, admin_only

@admin_only
def professor_list(request):
    professors = Professor.objects.all()
    return render(request, 'professors/list.html', {'professors': professors})


@login_required
@professor_only
def my_dashboard(request):
    professor_id = request.session.get('professor_id')
    professor = get_object_or_404(Professor, professorid=professor_id)
    sections = ClassSection.objects.filter(professorid=professor)
    return render(request, 'professors/my_dashboard.html', {
        'professor': professor,
        'sections': sections,
    })


@login_required
@professor_only
def my_courses(request):
    professor_id = request.session.get('professor_id')
    professor = get_object_or_404(Professor, professorid=professor_id)
    sections = ClassSection.objects.filter(professorid=professor).select_related('courseid')
    return render(request, 'professors/my_courses.html', {
        'professor': professor,
        'sections': sections,
    })


@login_required
@professor_only
def my_students(request):
    professor_id = request.session.get('professor_id')
    professor = get_object_or_404(Professor, professorid=professor_id)
    sections = ClassSection.objects.filter(professorid=professor)
    enrollments = Enrollment.objects.filter(sectionid__in=sections).select_related('studentid', 'sectionid__courseid')
    return render(request, 'professors/my_students.html', {
        'professor': professor,
        'enrollments': enrollments,
    })