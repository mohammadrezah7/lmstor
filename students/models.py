from django.db import models


class Student(models.Model):
    studentid = models.AutoField(db_column='StudentID', primary_key=True)
    firstname = models.CharField(db_column='FirstName', max_length=50, verbose_name='نام')
    lastname = models.CharField(db_column='LastName', max_length=50, verbose_name='نام خانوادگی')
    birthdate = models.DateField(db_column='BirthDate', blank=True, null=True, verbose_name='تاریخ تولد')
    gender = models.CharField(db_column='Gender', max_length=3, blank=True, null=True, verbose_name='جنسیت')
    nationalid = models.CharField(db_column='NationalID', unique=True, max_length=10, blank=True, null=True, verbose_name='کد ملی')
    email = models.CharField(db_column='Email', unique=True, max_length=100, blank=True, null=True, verbose_name='ایمیل')
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=15, blank=True, null=True, verbose_name='شماره تماس')
    enrollmentyear = models.TextField(db_column='EnrollmentYear', blank=True, null=True, verbose_name='سال ورود')
    programid = models.ForeignKey('courses.Program', models.DO_NOTHING, db_column='ProgramID', blank=True, null=True, verbose_name='رشته تحصیلی')
    gpa = models.DecimalField(db_column='GPA', max_digits=4, decimal_places=2, blank=True, null=True, verbose_name='معدل')
    accommodationid = models.ForeignKey('accommodation.Accommodation', models.DO_NOTHING, db_column='AccommodationID', blank=True, null=True, verbose_name='خوابگاه')

    class Meta:
        managed = False
        db_table = 'student'
        verbose_name = 'دانشجو'
        verbose_name_plural = 'دانشجویان'

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    def get_full_name(self):
        return f'{self.firstname} {self.lastname}'