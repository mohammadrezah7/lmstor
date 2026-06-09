from django.shortcuts import render
from .models import Tuition

def tuition_list(request):
    tuitions = Tuition.objects.all()
    return render(request, 'tuition/list.html', {'tuitions': tuitions})