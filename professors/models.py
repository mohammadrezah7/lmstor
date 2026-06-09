from django.db import models


class Professor(models.Model):
    professorid = models.AutoField(db_column='ProfessorID', primary_key=True)
    firstname = models.CharField(db_column='FirstName', max_length=50, verbose_name='نام')
    lastname = models.CharField(db_column='LastName', max_length=50, verbose_name='نام خانوادگی')
    academicrank = models.CharField(db_column='AcademicRank', max_length=8, verbose_name='رتبه علمی')
    department = models.CharField(db_column='Department', max_length=100, blank=True, null=True, verbose_name='دپارتمان')
    email = models.CharField(db_column='Email', unique=True, max_length=100, blank=True, null=True, verbose_name='ایمیل')
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=15, blank=True, null=True, verbose_name='شماره تماس')
    hiredate = models.DateField(db_column='HireDate', blank=True, null=True, verbose_name='تاریخ استخدام')

    class Meta:
        managed = False
        db_table = 'professor'
        verbose_name = 'استاد'
        verbose_name_plural = 'اساتید'

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    def get_full_name(self):
        return f'{self.firstname} {self.lastname}'