from django.db import models


class Alumni(models.Model):
    alumniid = models.AutoField(db_column='AlumniID', primary_key=True)
    studentid = models.OneToOneField('students.Student', models.DO_NOTHING, db_column='StudentID', blank=True, null=True, verbose_name='دانشجو')
    graduationyear = models.TextField(db_column='GraduationYear', blank=True, null=True, verbose_name='سال فارغ‌التحصیلی')
    degree = models.CharField(db_column='Degree', max_length=50, blank=True, null=True, verbose_name='مدرک')
    currentjob = models.CharField(db_column='CurrentJob', max_length=100, blank=True, null=True, verbose_name='شغل فعلی')
    employer = models.CharField(db_column='Employer', max_length=100, blank=True, null=True, verbose_name='کارفرما')

    class Meta:
        managed = False
        db_table = 'alumni'
        verbose_name = 'فارغ‌التحصیل'
        verbose_name_plural = 'فارغ‌التحصیلان'

    def __str__(self):
        return f'{self.studentid} - {self.degree}'