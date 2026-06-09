from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Student
from courses.models import Program


def student_list(request):
    students = Student.objects.select_related('programid', 'accommodationid').all()
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(firstname__icontains=search_query) |
            Q(lastname__icontains=search_query) |
            Q(nationalid__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Filters
    program_filter = request.GET.get('program', '')
    gender_filter = request.GET.get('gender', '')
    year_filter = request.GET.get('year', '')
    
    if program_filter:
        students = students.filter(programid_id=program_filter)
    if gender_filter:
        students = students.filter(gender=gender_filter)
    if year_filter:
        students = students.filter(enrollmentyear=year_filter)
    
    # Sorting
    sort_by = request.GET.get('sort', '-studentid')
    allowed_sorts = ['studentid', '-studentid', 'firstname', '-firstname', 
                     'lastname', '-lastname', 'gpa', '-gpa', 'enrollmentyear', '-enrollmentyear']
    if sort_by not in allowed_sorts:
        sort_by = '-studentid'
    students = students.order_by(sort_by)
    
    # Pagination (12 students per page)
    paginator = Paginator(students, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all programs for filter dropdown
    programs = Program.objects.all()
    
    # Get unique enrollment years for filter
    years = Student.objects.values_list('enrollmentyear', flat=True).distinct().order_by('-enrollmentyear')
    
    context = {
        'page_obj': page_obj,
        'students': page_obj,
        'total_students': students.count(),
        'programs': programs,
        'years': years,
        'search_query': search_query,
        'program_filter': program_filter,
        'gender_filter': gender_filter,
        'year_filter': year_filter,
        'sort_by': sort_by,
    }
    return render(request, 'students/list.html', context)


def student_detail(request, pk):
    student = get_object_or_404(Student.objects.select_related(
        'programid', 'accommodationid'
    ).prefetch_related(
        'enrollment_set__sectionid__courseid',
        'tuition_set',
        'societymembership_set__societyid',
    ), pk=pk)
    
    context = {
        'student': student,
        'enrollments': student.enrollment_set.all(),
        'tuitions': student.tuition_set.all().order_by('-year', '-tuitionid'),
        'society_memberships': student.societymembership_set.all(),
    }
    return render(request, 'students/detail.html', context)


def student_create(request):
    if request.method == 'POST':
        pass
    programs = Program.objects.all()
    return render(request, 'students/form.html', {'programs': programs})