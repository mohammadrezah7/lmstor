from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.book_list, name='list'),
    path('<int:pk>/', views.book_detail, name='detail'),
    path('<int:pk>/issue/', views.issue_book, name='issue_book'),
    path('<int:pk>/return/<int:loan_id>/', views.return_book, name='return_book'),
    path('loans/', views.all_loans, name='loans'),
    path('my-loans/', views.my_loans, name='my_loans'),
]