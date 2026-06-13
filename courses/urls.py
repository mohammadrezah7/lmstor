from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Programs
    path('programs/', views.program_list, name='programs'),
    path('programs/<int:pk>/', views.program_detail, name='program_detail'),
    
    # Courses
    path('', views.course_list, name='list'),
    path('<int:pk>/', views.course_detail, name='detail'),
    
    # Sections
    path('sections/', views.section_list, name='sections'),
    path('sections/create/', views.section_create, name='section_create'),
    path('sections/<int:pk>/', views.section_detail, name='section_detail'),
    path('sections/<int:section_id>/enroll/', views.enroll_student, name='enroll_student'),
    path('enrollment/<int:enrollment_id>/grade/', views.set_grade, name='set_grade'),
    path('enrollment/<int:enrollment_id>/remove/', views.remove_enrollment, name='remove_enrollment'),
]