from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm
from courses.models import Program
from accounts.decorators import student_only, admin_only, admin_or_professor

@admin_or_professor
def student_list(request):
    students = Student.objects.select_related('programid', 'accommodationid').all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(firstname__icontains=search_query) |
            Q(lastname__icontains=search_query) |
            Q(nationalid__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    program_filter = request.GET.get('program', '')
    gender_filter = request.GET.get('gender', '')
    year_filter = request.GET.get('year', '')
    
    if program_filter:
        students = students.filter(programid_id=program_filter)
    if gender_filter:
        students = students.filter(gender=gender_filter)
    if year_filter:
        students = students.filter(enrollmentyear=year_filter)
    
    sort_by = request.GET.get('sort', '-studentid')
    allowed_sorts = ['studentid', '-studentid', 'firstname', '-firstname', 
                     'lastname', '-lastname', 'gpa', '-gpa', 'enrollmentyear', '-enrollmentyear']
    if sort_by not in allowed_sorts:
        sort_by = '-studentid'
    students = students.order_by(sort_by)
    
    paginator = Paginator(students, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    programs = Program.objects.all()
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

@admin_or_professor
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


@login_required
@admin_only
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'✅ دانشجوی "{student.get_full_name()}" با موفقیت افزوده شد.')
            return redirect('students:detail', pk=student.studentid)
        else:
            messages.error(request, '❌ لطفاً خطاهای فرم را اصلاح کنید.')
    else:
        form = StudentForm()
    
    return render(request, 'students/form.html', {
        'form': form,
        'title': 'افزودن دانشجوی جدید',
        'action': 'create'
    })


@login_required
@admin_only
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ اطلاعات "{student.get_full_name()}" با موفقیت بروزرسانی شد.')
            return redirect('students:detail', pk=student.studentid)
        else:
            messages.error(request, '❌ لطفاً خطاهای فرم را اصلاح کنید.')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'students/form.html', {
        'form': form,
        'title': f'ویرایش اطلاعات: {student.get_full_name()}',
        'action': 'update',
        'student': student
    })


@login_required
@admin_only
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        name = student.get_full_name()
        student.delete()
        messages.success(request, f'🗑️ دانشجوی "{name}" با موفقیت حذف شد.')
        return redirect('students:list')
    
    return render(request, 'students/delete.html', {'student': student})


# ============ STUDENT PANEL VIEWS ============

@login_required
@student_only
def my_dashboard(request):
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, studentid=student_id)
    context = {
        'student': student,
        'enrollments': student.enrollment_set.all(),
    }
    return render(request, 'students/my_dashboard.html', context)


@login_required
@student_only
def my_courses(request):
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, studentid=student_id)
    enrollments = student.enrollment_set.all()
    return render(request, 'students/my_courses.html', {'student': student, 'enrollments': enrollments})


@login_required
@student_only
def my_grades(request):
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, studentid=student_id)
    enrollments = student.enrollment_set.all()
    return render(request, 'students/my_grades.html', {'student': student, 'enrollments': enrollments})


@login_required
@student_only
def my_tuition(request):
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, studentid=student_id)
    tuitions = student.tuition_set.all().order_by('-year', '-tuitionid')
    return render(request, 'students/my_tuition.html', {'student': student, 'tuitions': tuitions})