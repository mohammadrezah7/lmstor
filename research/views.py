from django.shortcuts import render
from .models import Research

def research_list(request):
    researches = Research.objects.all()
    return render(request, 'research/list.html', {'researches': researches})