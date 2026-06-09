from django.shortcuts import render
from .models import Society

def society_list(request):
    societies = Society.objects.all()
    return render(request, 'societies/list.html', {'societies': societies})