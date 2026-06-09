from django.shortcuts import render
from .models import Program, Course


def program_list(request):
    programs = Program.objects.all()
    return render(request, 'courses/programs.html', {'programs': programs})


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/list.html', {'courses': courses})