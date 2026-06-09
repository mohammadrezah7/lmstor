from django.db import models


class Library(models.Model):
    bookid = models.AutoField(db_column='BookID', primary_key=True)
    title = models.CharField(db_column='Title', max_length=200, verbose_name='عنوان کتاب')
    author = models.CharField(db_column='Author', max_length=100, blank=True, null=True, verbose_name='نویسنده')
    publisher = models.CharField(db_column='Publisher', max_length=100, blank=True, null=True, verbose_name='ناشر')
    year = models.TextField(db_column='Year', blank=True, null=True, verbose_name='سال انتشار')
    isbn = models.CharField(db_column='ISBN', unique=True, max_length=20, blank=True, null=True, verbose_name='شابک')
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True, verbose_name='دسته‌بندی')
    copiesavailable = models.IntegerField(db_column='CopiesAvailable', blank=True, null=True, verbose_name='تعداد موجود')

    class Meta:
        managed = False
        db_table = 'library'
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب‌ها'

    def __str__(self):
        return self.title


class Loan(models.Model):
    loanid = models.AutoField(db_column='LoanID', primary_key=True)
    bookid = models.ForeignKey(Library, models.DO_NOTHING, db_column='BookID', blank=True, null=True, verbose_name='کتاب')
    borrowerid = models.IntegerField(db_column='BorrowerID', blank=True, null=True, verbose_name='شناسه امانت‌گیرنده')
    borrowertype = models.CharField(db_column='BorrowerType', max_length=9, verbose_name='نوع امانت‌گیرنده')
    loandate = models.DateField(db_column='LoanDate', blank=True, null=True, verbose_name='تاریخ امانت')
    returndate = models.DateField(db_column='ReturnDate', blank=True, null=True, verbose_name='تاریخ بازگشت')

    class Meta:
        managed = False
        db_table = 'loan'
        verbose_name = 'امانت کتاب'
        verbose_name_plural = 'امانت‌های کتاب'

    def __str__(self):
        return f'{self.bookid} - {self.borrowertype} #{self.borrowerid}'