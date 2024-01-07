from django.db import models


class TimeModel(models.Model):
    time_id = models.AutoField(primary_key=True)
    year = models.IntegerField()
    quarter = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    minute = models.IntegerField()

    objects = models.Manager()

    class Meta:
        db_table = 'dim_time'
        app_label = 'spacetravel'
