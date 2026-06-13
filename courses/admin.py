from django.contrib import admin
from .models import Program, Course, ClassSection, Enrollment


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['programid', 'programname', 'degreelevel', 'department', 'duration']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['courseid', 'coursename', 'credits', 'department', 'programid']


@admin.register(ClassSection)
class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ['sectionid', 'courseid', 'professorid', 'semester', 'year', 'classroom', 'capacity']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['enrollmentid', 'studentid', 'sectionid', 'grade']