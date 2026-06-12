from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='list'),
    path('<int:pk>/', views.student_detail, name='detail'),
    path('create/', views.student_create, name='create'),
    path('my-dashboard/', views.my_dashboard, name='my_dashboard'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('my-grades/', views.my_grades, name='my_grades'),
    path('my-tuition/', views.my_tuition, name='my_tuition'),
]