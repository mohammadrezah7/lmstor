from django.urls import path
from . import views

app_name = 'societies'
urlpatterns = [path('', views.society_list, name='list')]