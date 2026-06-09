from django.shortcuts import render
from .models import Professor


def professor_list(request):
    professors = Professor.objects.all()
    return render(request, 'professors/list.html', {'professors': professors})