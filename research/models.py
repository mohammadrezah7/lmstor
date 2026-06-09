from django.db import models


class Research(models.Model):
    researchid = models.AutoField(db_column='ResearchID', primary_key=True)
    title = models.CharField(db_column='Title', max_length=200, verbose_name='عنوان پژوهش')
    field = models.CharField(db_column='Field', max_length=100, blank=True, null=True, verbose_name='زمینه')
    startdate = models.DateField(db_column='StartDate', blank=True, null=True, verbose_name='تاریخ شروع')
    enddate = models.DateField(db_column='EndDate', blank=True, null=True, verbose_name='تاریخ پایان')
    funding = models.DecimalField(db_column='Funding', max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='بودجه')
    description = models.TextField(db_column='Description', blank=True, null=True, verbose_name='توضیحات')

    class Meta:
        managed = False
        db_table = 'research'
        verbose_name = 'پژوهش'
        verbose_name_plural = 'پژوهش‌ها'

    def __str__(self):
        return self.title


class ResearchParticipant(models.Model):
    participationid = models.AutoField(db_column='ParticipationID', primary_key=True)
    researchid = models.ForeignKey(Research, models.DO_NOTHING, db_column='ResearchID', blank=True, null=True, verbose_name='پژوهش')
    participantid = models.IntegerField(db_column='ParticipantID', blank=True, null=True, verbose_name='شناسه شرکت‌کننده')
    participanttype = models.CharField(db_column='ParticipantType', max_length=9, verbose_name='نوع شرکت‌کننده')
    role = models.CharField(db_column='Role', max_length=50, blank=True, null=True, verbose_name='نقش')

    class Meta:
        managed = False
        db_table = 'researchparticipant'
        verbose_name = 'شرکت‌کننده پژوهش'
        verbose_name_plural = 'شرکت‌کنندگان پژوهش'

    def __str__(self):
        return f'{self.researchid} - {self.participanttype} #{self.participantid}'