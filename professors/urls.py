from django.urls import path
from . import views

app_name = 'professors'

urlpatterns = [
    path('', views.professor_list, name='list'),
    path('my-dashboard/', views.my_dashboard, name='my_dashboard'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('my-students/', views.my_students, name='my_students'),
]