from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_only
from django.db.models import Count, Sum
from students.models import Student
from professors.models import Professor
from library.models import Library, Loan
from research.models import Research
from courses.models import Course
from tuition.models import Tuition


@login_required
def dashboard(request):
    # اگه ادمین نیست، بفرست به داشبورد خودش
    role = request.session.get('role', None)
    
    if role == 'student':
        return redirect('students:my_dashboard')
    elif role == 'professor':
        return redirect('professors:my_dashboard')
    
    # فقط ادمین ادامه میده
    context = {
        'total_students': Student.objects.count(),
        'total_professors': Professor.objects.count(),
        'total_books': Library.objects.count(),
        'total_courses': Course.objects.count(),
        'total_research': Research.objects.count(),
        'active_loans': Loan.objects.filter(returndate__isnull=True).count(),
        'total_tuition_paid': Tuition.objects.filter(paymentstatus='پرداخت شده').aggregate(Sum('amount'))['amount__sum'] or 0,
        'recent_students': Student.objects.all().order_by('-studentid')[:5],
        'recent_loans': Loan.objects.select_related('bookid').all().order_by('-loanid')[:5],
    }
    return render(request, 'core/dashboard.html', context)