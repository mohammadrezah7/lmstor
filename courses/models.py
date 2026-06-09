from django.db import models


class Program(models.Model):
    programid = models.AutoField(db_column='ProgramID', primary_key=True)
    programname = models.CharField(db_column='ProgramName', max_length=100, verbose_name='نام رشته')
    degreelevel = models.CharField(db_column='DegreeLevel', max_length=13, verbose_name='مقطع')
    department = models.CharField(db_column='Department', max_length=100, blank=True, null=True, verbose_name='دپارتمان')
    duration = models.IntegerField(db_column='Duration', blank=True, null=True, verbose_name='مدت تحصیل (سال)')

    class Meta:
        managed = False
        db_table = 'program'
        verbose_name = 'رشته تحصیلی'
        verbose_name_plural = 'رشته‌های تحصیلی'

    def __str__(self):
        return f'{self.programname} ({self.degreelevel})'


class Course(models.Model):
    courseid = models.AutoField(db_column='CourseID', primary_key=True)
    coursename = models.CharField(db_column='CourseName', max_length=100, verbose_name='نام درس')
    credits = models.IntegerField(db_column='Credits', verbose_name='تعداد واحد')
    department = models.CharField(db_column='Department', max_length=100, blank=True, null=True, verbose_name='دپارتمان')
    programid = models.ForeignKey(Program, models.DO_NOTHING, db_column='ProgramID', blank=True, null=True, verbose_name='رشته')

    class Meta:
        managed = False
        db_table = 'course'
        verbose_name = 'درس'
        verbose_name_plural = 'دروس'

    def __str__(self):
        return f'{self.coursename} ({self.credits} واحد)'


class ClassSection(models.Model):
    sectionid = models.AutoField(db_column='SectionID', primary_key=True)
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='CourseID', blank=True, null=True, verbose_name='درس')
    professorid = models.ForeignKey('professors.Professor', models.DO_NOTHING, db_column='ProfessorID', blank=True, null=True, verbose_name='استاد')
    semester = models.CharField(db_column='Semester', max_length=7, verbose_name='ترم')
    year = models.TextField(db_column='Year', blank=True, null=True, verbose_name='سال')
    classroom = models.CharField(db_column='Classroom', max_length=50, blank=True, null=True, verbose_name='کلاس')
    capacity = models.IntegerField(db_column='Capacity', blank=True, null=True, verbose_name='ظرفیت')

    class Meta:
        managed = False
        db_table = 'classsection'
        verbose_name = 'گروه درسی'
        verbose_name_plural = 'گروه‌های درسی'

    def __str__(self):
        return f'{self.courseid} - {self.semester} {self.year}'


class Enrollment(models.Model):
    enrollmentid = models.AutoField(db_column='EnrollmentID', primary_key=True)
    studentid = models.ForeignKey('students.Student', models.DO_NOTHING, db_column='StudentID', blank=True, null=True, verbose_name='دانشجو')
    sectionid = models.ForeignKey(ClassSection, models.DO_NOTHING, db_column='SectionID', blank=True, null=True, verbose_name='گروه درسی')
    grade = models.DecimalField(db_column='Grade', max_digits=4, decimal_places=2, blank=True, null=True, verbose_name='نمره')

    class Meta:
        managed = False
        db_table = 'enrollment'
        verbose_name = 'ثبت‌نام'
        verbose_name_plural = 'ثبت‌نام‌ها'

    def __str__(self):
        return f'{self.studentid} - {self.sectionid}'