from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Library, Loan
from students.models import Student
from professors.models import Professor
from django.db.models import Q
from accounts.decorators import admin_only, admin_or_professor, student_only


def book_list(request):
    books = Library.objects.all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search) |
            Q(isbn__icontains=search) |
            Q(category__icontains=search)
        )
    
    # Category filter
    category = request.GET.get('category', '')
    categories = Library.objects.values_list('category', flat=True).distinct()
    if category:
        books = books.filter(category=category)
    
    # Active loans count
    active_loans = Loan.objects.filter(returndate__isnull=True).count()
    
    context = {
        'books': books,
        'categories': categories,
        'category_filter': category,
        'search_query': search,
        'active_loans': active_loans,
    }
    return render(request, 'library/list.html', context)


@login_required
@admin_or_professor
def book_detail(request, pk):
    book = get_object_or_404(Library, pk=pk)
    loans = Loan.objects.filter(bookid=book).order_by('-loanid')
    active_loan = Loan.objects.filter(bookid=book, returndate__isnull=True).first()
    
    students = Student.objects.all()
    professors = Professor.objects.all()
    
    context = {
        'book': book,
        'loans': loans,
        'active_loan': active_loan,
        'students': students,
        'professors': professors,
    }
    return render(request, 'library/detail.html', context)


@login_required
@admin_or_professor
def issue_book(request, pk):
    """امانت دادن کتاب"""
    if request.method == 'POST':
        book = get_object_or_404(Library, pk=pk)
        borrower_type = request.POST.get('borrower_type')
        borrower_id = request.POST.get('borrower_id')
        
        # Check if book is available
        if book.copiesavailable and book.copiesavailable > 0:
            # Check if already borrowed by this person
            existing = Loan.objects.filter(
                bookid=book,
                borrowerid=borrower_id,
                borrowertype=borrower_type,
                returndate__isnull=True
            ).exists()
            
            if existing:
                messages.warning(request, '⚠️ این شخص قبلاً این کتاب را امانت گرفته است!')
            else:
                Loan.objects.create(
                    bookid=book,
                    borrowerid=borrower_id,
                    borrowertype=borrower_type,
                    loandate=timezone.now().date()
                )
                # Decrease available copies
                book.copiesavailable -= 1
                book.save()
                messages.success(request, f'✅ کتاب "{book.title}" با موفقیت امانت داده شد.')
        else:
            messages.error(request, '❌ این کتاب در حال حاضر موجود نیست!')
    
    return redirect('library:detail', pk=pk)


@login_required
@admin_or_professor
def return_book(request, pk, loan_id):
    """برگشت کتاب"""
    loan = get_object_or_404(Loan, pk=loan_id, bookid_id=pk)
    
    if loan.returndate:
        messages.info(request, 'این کتاب قبلاً برگشت داده شده است.')
    else:
        loan.returndate = timezone.now().date()
        loan.save()
        
        # Increase available copies
        book = loan.bookid
        if book.copiesavailable is not None:
            book.copiesavailable += 1
            book.save()
        
        messages.success(request, f'✅ کتاب "{book.title}" با موفقیت برگشت داده شد.')
    
    return redirect('library:detail', pk=pk)


@login_required
@admin_or_professor
def all_loans(request):
    """لیست همه امانت‌ها"""
    loans = Loan.objects.select_related('bookid').all().order_by('-loanid')
    
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        loans = loans.filter(returndate__isnull=True)
    elif status_filter == 'returned':
        loans = loans.filter(returndate__isnull=False)
    
    context = {
        'loans': loans,
        'status_filter': status_filter,
    }
    return render(request, 'library/loans.html', context)


@login_required
@student_only
def my_loans(request):
    """امانت‌های کاربر جاری"""
    student_id = request.session.get('student_id')
    professor_id = request.session.get('professor_id')
    
    loans = Loan.objects.select_related('bookid').all()
    
    if student_id:
        loans = loans.filter(borrowerid=student_id, borrowertype='Student')
    elif professor_id:
        loans = loans.filter(borrowerid=professor_id, borrowertype='Professor')
    else:
        loans = Loan.objects.none()
    
    return render(request, 'library/my_loans.html', {'loans': loans.order_by('-loanid')})