from django.db import models


class Time(models.Model):
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


class Magnitude(models.Model):
    magnitude_id = models.AutoField(primary_key=True)
    magnitude = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()

    class Meta:
        db_table = 'dim_magnitude'
        app_label = 'spacetravel'


class Type(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.TextField()
    description = models.TextField()
    class_range = models.TextField()

    objects = models.Manager()

    class Meta:
        db_table = 'dim_type'
        app_label = 'spacetravel'


class Diameter(models.Model):
    diameter_id = models.AutoField(primary_key=True)
    kilometer = models.DecimalField(max_digits=10, decimal_places=2)
    meter = models.DecimalField(max_digits=10, decimal_places=2)
    miles = models.DecimalField(max_digits=10, decimal_places=2)
    feet = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()

    class Meta:
        db_table = 'dim_diameter'
        app_label = 'spacetravel'


class Asteroid(models.Model):
    asteroid_id = models.AutoField(primary_key=True)
    is_potentially_hazardous = models.BooleanField()
    is_sentry_object = models.BooleanField()
    arc_in_days = models.IntegerField()
    minimum_orbit_intersection = models.DecimalField(max_digits=10, decimal_places=2)
    epoch_osculation = models.DecimalField(max_digits=10, decimal_places=2)
    eccentricity = models.DecimalField(max_digits=10, decimal_places=2)
    semi_major_axis = models.DecimalField(max_digits=10, decimal_places=2)
    inclination = models.DecimalField(max_digits=10, decimal_places=2)
    ascending_node_longitude = models.DecimalField(max_digits=10, decimal_places=2)
    orbital_period = models.DecimalField(max_digits=10, decimal_places=2)
    perihelion_distance = models.DecimalField(max_digits=10, decimal_places=2)
    perihelion_argument = models.DecimalField(max_digits=10, decimal_places=2)
    mean_anomaly = models.DecimalField(max_digits=10, decimal_places=2)
    mean_motion = models.DecimalField(max_digits=10, decimal_places=2)
    orbit_determination_date = models.DateTimeField()

    objects = models.Manager()

    class Meta:
        db_table = 'dim_asteroid_detail'
        app_label = 'spacetravel'


class FactSheet(models.Model):
    fact_sheet_id = models.AutoField(primary_key=True)
    time_id = models.ForeignKey(Time, on_delete=models.CASCADE, db_column='time_id')
    diameter_id = models.ForeignKey(Diameter, on_delete=models.CASCADE, db_column='diameter_id')
    magnitude_id = models.ForeignKey(Magnitude, on_delete=models.CASCADE, db_column='magnitude_id')
    asteroid_id = models.ForeignKey(Asteroid, on_delete=models.CASCADE, db_column='asteroid_id')
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE, db_column='type_id')
    asteroid_name = models.TextField()

    objects = models.Manager()

    class Meta:
        db_table = 'fact_asteroid'
        app_label = 'spacetravel'
