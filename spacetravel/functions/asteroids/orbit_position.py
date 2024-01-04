from astropy.time import Time
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from spacetravel.models.neo import FactSheet
import astropy.units as u


def calculate_current_orbit(neo_data):
    # Convert angle values to radians
    inclination = neo_data.inclination * u.deg
    ascending_node = neo_data.ascending_node_longitude * u.deg
    perihelion_arg = neo_data.perihelion_argument * u.deg
    mean_anomaly = neo_data.mean_anomaly * u.deg

    orb = Orbit.from_classical(
        Earth,
        a=neo_data.semi_major_axis * u.AU,
        ecc=neo_data.eccentricity * u.one,
        inc=inclination,
        raan=ascending_node,
        argp=perihelion_arg,
        nu=mean_anomaly,
        epoch=Time(neo_data.epoch_osculation, format='jd')
    )

    time_since_closest_approach = get_closets_time(neo_data.asteroid_id)
    orb_at_current_time = orb.propagate(time_since_closest_approach)
    x, y, z = orb_at_current_time.r

    return x.to(u.km), y.to(u.km), z.to(u.km)


def get_closets_time(asteroid_id):
    current_time = Time.now()

    time_filter_query = f'''
                WITH ranked_asteroids AS (
                    SELECT f.*,
                        MAKE_TIMESTAMP(t.year, t.month, t.day, t.hour, t.minute, 0) as temp_timestamp,
                        RANK() OVER (PARTITION BY f.asteroid_id ORDER BY ABS(EXTRACT(EPOCH FROM (
                            MAKE_TIMESTAMP(t.year, t.month, t.day, t.hour, t.minute, 0) - NOW()
                        )))) AS rank
                    FROM fact_asteroid f
                    JOIN dim_time t ON f.time_id = t.time_id
                    WHERE
                        f.asteroid_id = {asteroid_id} AND 
                        MAKE_TIMESTAMP(t.year, t.month, t.day, t.hour, t.minute, 0) < NOW()
                )
                SELECT * FROM ranked_asteroids WHERE rank = 1;
                '''

    raw_results = FactSheet.objects.using('neo').raw(time_filter_query)
    if len(raw_results) > 0:
        temp_timestamp = Time(raw_results[0].temp_timestamp)
    else:
        temp_timestamp = Time("2023-12-11 05:31:18", format='iso')

    return current_time - temp_timestamp


def get_closest_approach(asteroid_id):
    time_filter_query = f''' WITH ranked_asteroids AS ( SELECT f.*, MAKE_TIMESTAMP(t.year, t.month, t.day, t.hour, 
    t.minute, 0) as temp_timestamp, RANK() OVER (PARTITION BY f.asteroid_id ORDER BY ABS(EXTRACT(EPOCH FROM ( 
    MAKE_TIMESTAMP(t.year, t.month, CASE WHEN t.day = 1 THEN 28 ELSE t.day-1 END, t.hour, t.minute, 0) - NOW() )))) 
    AS rank 
    FROM fact_asteroid f JOIN dim_time t ON f.time_id = t.time_id 
    WHERE f.asteroid_id = {asteroid_id} AND MAKE_TIMESTAMP(t.year, t.month, 
        CASE WHEN t.day = 1 THEN 28 ELSE t.day-1 END, 
        t.hour, t.minute, 0) > NOW() ) 
    SELECT * FROM ranked_asteroids WHERE rank = 1;'''

    raw_results = FactSheet.objects.using('neo').raw(time_filter_query)
    if len(raw_results) > 0:
        temp_timestamp = str(Time(raw_results[0].temp_timestamp))
    else:
        temp_timestamp = "Unknown"

    return temp_timestamp
