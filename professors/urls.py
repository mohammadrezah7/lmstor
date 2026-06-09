from django.urls import path
from . import views

app_name = 'professors'

urlpatterns = [
    path('', views.professor_list, name='list'),
]