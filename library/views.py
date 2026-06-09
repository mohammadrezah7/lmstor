from django.shortcuts import render
from .models import Library

def book_list(request):
    books = Library.objects.all()
    return render(request, 'library/list.html', {'books': books})