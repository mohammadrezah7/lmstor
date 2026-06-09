from django.db import models


class Accommodation(models.Model):
    accommodationid = models.AutoField(db_column='AccommodationID', primary_key=True)
    dormitoryname = models.CharField(db_column='DormitoryName', max_length=100, verbose_name='نام خوابگاه')
    roomnumber = models.CharField(db_column='RoomNumber', max_length=10, blank=True, null=True, verbose_name='شماره اتاق')
    capacity = models.IntegerField(db_column='Capacity', blank=True, null=True, verbose_name='ظرفیت')
    location = models.CharField(db_column='Location', max_length=100, blank=True, null=True, verbose_name='موقعیت')

    class Meta:
        managed = False
        db_table = 'accommodation'
        verbose_name = 'خوابگاه'
        verbose_name_plural = 'خوابگاه‌ها'

    def __str__(self):
        return f'{self.dormitoryname} - اتاق {self.roomnumber}'