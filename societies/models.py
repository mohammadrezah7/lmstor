from django.db import models


class Society(models.Model):
    societyid = models.AutoField(db_column='SocietyID', primary_key=True)
    societyname = models.CharField(db_column='SocietyName', max_length=100, verbose_name='نام انجمن')
    type = models.CharField(db_column='Type', max_length=6, verbose_name='نوع')
    establishmentyear = models.TextField(db_column='EstablishmentYear', blank=True, null=True, verbose_name='سال تأسیس')
    advisorprofessor = models.ForeignKey('professors.Professor', models.DO_NOTHING, db_column='AdvisorProfessor', blank=True, null=True, verbose_name='استاد مشاور')
    description = models.TextField(db_column='Description', blank=True, null=True, verbose_name='توضیحات')

    class Meta:
        managed = False
        db_table = 'society'
        verbose_name = 'انجمن'
        verbose_name_plural = 'انجمن‌ها'

    def __str__(self):
        return self.societyname


class SocietyMembership(models.Model):
    membershipid = models.AutoField(db_column='MembershipID', primary_key=True)
    studentid = models.ForeignKey('students.Student', models.DO_NOTHING, db_column='StudentID', blank=True, null=True, verbose_name='دانشجو')
    societyid = models.ForeignKey(Society, models.DO_NOTHING, db_column='SocietyID', blank=True, null=True, verbose_name='انجمن')
    joindate = models.DateField(db_column='JoinDate', blank=True, null=True, verbose_name='تاریخ عضویت')

    class Meta:
        managed = False
        db_table = 'societymembership'
        verbose_name = 'عضویت در انجمن'
        verbose_name_plural = 'عضویت‌های انجمن'

    def __str__(self):
        return f'{self.studentid} - {self.societyid}'