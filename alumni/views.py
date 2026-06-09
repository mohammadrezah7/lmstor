from django.shortcuts import render
from .models import Alumni

def alumni_list(request):
    alumnis = Alumni.objects.all()
    return render(request, 'alumni/list.html', {'alumnis': alumnis})