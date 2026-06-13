from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Program, Course, ClassSection, Enrollment
from professors.models import Professor
from students.models import Student
from accounts.decorators import admin_only, admin_or_professor


# ============ PROGRAMS ============

def program_list(request):
    programs = Program.objects.annotate(student_count=Count('student'))
    return render(request, 'courses/programs.html', {'programs': programs})


def program_detail(request, pk):
    program = get_object_or_404(Program, pk=pk)
    students = Student.objects.filter(programid=program)
    courses = Course.objects.filter(programid=program)
    return render(request, 'courses/program_detail.html', {
        'program': program,
        'students': students,
        'courses': courses,
    })


# ============ COURSES ============

def course_list(request):
    courses = Course.objects.select_related('programid').all()
    return render(request, 'courses/list.html', {'courses': courses})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    sections = ClassSection.objects.filter(courseid=course).select_related('professorid')
    return render(request, 'courses/detail.html', {
        'course': course,
        'sections': sections,
    })


# ============ CLASS SECTIONS ============
@admin_or_professor
def section_list(request):
    sections = ClassSection.objects.select_related('courseid', 'professorid').all()
    
    semester_filter = request.GET.get('semester', '')
    if semester_filter:
        sections = sections.filter(semester=semester_filter)
    
    return render(request, 'courses/sections.html', {
        'sections': sections,
        'semester_filter': semester_filter,
    })

@admin_or_professor
def section_detail(request, pk):
    section = get_object_or_404(ClassSection.objects.select_related('courseid', 'professorid'), pk=pk)
    enrollments = Enrollment.objects.filter(sectionid=section).select_related('studentid')
    available_seats = section.capacity - enrollments.count() if section.capacity else None
    
    all_students = Student.objects.all()
    
    return render(request, 'courses/section_detail.html', {
        'section': section,
        'enrollments': enrollments,
        'available_seats': available_seats,
        'all_students': all_students,
    })


@login_required
@admin_only
def section_create(request):
    if request.method == 'POST':
        course_id = request.POST.get('courseid')
        professor_id = request.POST.get('professorid')
        semester = request.POST.get('semester')
        year = request.POST.get('year')
        classroom = request.POST.get('classroom')
        capacity = request.POST.get('capacity')
        
        ClassSection.objects.create(
            courseid_id=course_id,
            professorid_id=professor_id,
            semester=semester,
            year=year,
            classroom=classroom,
            capacity=capacity
        )
        messages.success(request, '✅ گروه درسی با موفقیت ایجاد شد.')
        return redirect('courses:sections')
    
    courses = Course.objects.all()
    professors = Professor.objects.all()
    return render(request, 'courses/section_form.html', {
        'courses': courses,
        'professors': professors,
    })


@login_required
@admin_or_professor
def enroll_student(request, section_id):
    """ثبت‌نام دانشجو در کلاس"""
    section = get_object_or_404(ClassSection, pk=section_id)
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        
        # Check if already enrolled
        if Enrollment.objects.filter(sectionid=section, studentid_id=student_id).exists():
            messages.warning(request, '⚠️ این دانشجو قبلاً در این کلاس ثبت‌نام شده است.')
        else:
            # Check capacity
            enrolled_count = Enrollment.objects.filter(sectionid=section).count()
            if section.capacity and enrolled_count >= section.capacity:
                messages.error(request, '❌ ظرفیت کلاس تکمیل است!')
            else:
                Enrollment.objects.create(
                    studentid_id=student_id,
                    sectionid=section,
                )
                messages.success(request, '✅ دانشجو با موفقیت ثبت‌نام شد.')
    
    return redirect('courses:section_detail', pk=section_id)


@login_required
@admin_or_professor
def set_grade(request, enrollment_id):
    """ثبت نمره برای دانشجو"""
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    
    if request.method == 'POST':
        grade = request.POST.get('grade')
        enrollment.grade = grade
        enrollment.save()
        messages.success(request, f'✅ نمره با موفقیت ثبت شد.')
    
    return redirect('courses:section_detail', pk=enrollment.sectionid.sectionid)


@login_required
@admin_or_professor
def remove_enrollment(request, enrollment_id):
    """حذف ثبت‌نام"""
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    section_id = enrollment.sectionid.sectionid
    
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, '🗑️ ثبت‌نام با موفقیت حذف شد.')
    
    return redirect('courses:section_detail', pk=section_id)