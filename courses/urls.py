from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('programs/', views.program_list, name='programs'),
    path('', views.course_list, name='list'),
]