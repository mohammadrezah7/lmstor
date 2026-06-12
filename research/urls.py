from django.urls import path
from . import views

app_name = 'research'

urlpatterns = [
    path('', views.research_list, name='list'),
    path('my-research/', views.my_research, name='my_research'),
]