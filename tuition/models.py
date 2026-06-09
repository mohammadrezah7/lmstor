from django.db import models


class Tuition(models.Model):
    tuitionid = models.AutoField(db_column='TuitionID', primary_key=True)
    studentid = models.ForeignKey('students.Student', models.DO_NOTHING, db_column='StudentID', blank=True, null=True, verbose_name='دانشجو')
    semester = models.CharField(db_column='Semester', max_length=14, verbose_name='ترم')
    year = models.TextField(db_column='Year', blank=True, null=True, verbose_name='سال')
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='مبلغ')
    paymentstatus = models.CharField(db_column='PaymentStatus', max_length=11, verbose_name='وضعیت پرداخت')
    paymentdate = models.DateField(db_column='PaymentDate', blank=True, null=True, verbose_name='تاریخ پرداخت')
    paymentmethod = models.CharField(db_column='PaymentMethod', max_length=50, blank=True, null=True, verbose_name='روش پرداخت')
    description = models.TextField(db_column='Description', blank=True, null=True, verbose_name='توضیحات')

    class Meta:
        managed = False
        db_table = 'tuition'
        verbose_name = 'شهریه'
        verbose_name_plural = 'شهریه‌ها'

    def __str__(self):
        return f'{self.studentid} - {self.semester} {self.year}'