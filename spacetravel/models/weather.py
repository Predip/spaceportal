from django.db import models


class WeatherTime(models.Model):
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


class Plasma(models.Model):
    plasma_id = models.AutoField(primary_key=True)
    density = models.DecimalField(max_digits=10, decimal_places=2)
    speed = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()

    class Meta:
        db_table = 'dim_plasma'
        app_label = 'spacetravel'


class Magnetometer(models.Model):
    magnetometer_id = models.AutoField(primary_key=True)
    he = models.DecimalField(max_digits=10, decimal_places=2)
    hp = models.DecimalField(max_digits=10, decimal_places=2)
    hn = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()

    class Meta:
        db_table = 'dim_magnetometer'
        app_label = 'spacetravel'


class Mag(models.Model):
    mag_id = models.AutoField(primary_key=True)
    bx_gsm = models.DecimalField(max_digits=10, decimal_places=2)
    by_gsm = models.DecimalField(max_digits=10, decimal_places=2)
    bz_gsm = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()

    class Meta:
        db_table = 'dim_mag'
        app_label = 'spacetravel'


class Proton(models.Model):
    proton_id = models.AutoField(primary_key=True)
    flux = models.DecimalField(max_digits=10, decimal_places=2)
    energy = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()

    class Meta:
        db_table = 'dim_proton'
        app_label = 'spacetravel'


class WeatherSheet(models.Model):
    fact_sheet_id = models.AutoField(primary_key=True)
    plasma = models.ForeignKey(Plasma, on_delete=models.CASCADE)
    time = models.ForeignKey(WeatherTime, on_delete=models.CASCADE)
    magnetometer = models.ForeignKey(Magnetometer, on_delete=models.CASCADE)
    mag = models.ForeignKey(Mag, on_delete=models.CASCADE)
    proton = models.ForeignKey(Proton, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        db_table = 'fact_weather'
        app_label = 'spacetravel'
