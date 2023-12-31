from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from astropy.time import Time
import astropy.units as u


def calculate_current_orbit(neo_data):
    # Convert angle values to radians
    inclination = neo_data.inclination * u.deg
    ascending_node = neo_data.ascending_node_longitude * u.deg
    perihelion_arg = neo_data.perihelion_argument * u.deg
    mean_anomaly = neo_data.mean_anomaly * u.deg
    # true_anomaly = 0.0 * u.deg

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

    current_time = Time.now()
    closest_approach_time = Time("2023-12-11 05:31:18", format='iso')
    time_since_closest_approach = current_time - closest_approach_time
    orb_at_current_time = orb.propagate(time_since_closest_approach)
    x, y, z = orb_at_current_time.r

    return x.to(u.km), y.to(u.km), z.to(u.km)
