from django.urls import path
from . import views

app_name = 'tuition'
urlpatterns = [path('', views.tuition_list, name='list')]