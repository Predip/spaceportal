import json
from .functions.neo.orbit_position import calculate_current_orbit, get_closest_approach
from .functions.news.wordcloud_generator import WordCloudGenerator
# from .functions.weather import forecasting
from .models import Asteroid, NeoSheet, WeatherSheet
from django.db.models import F, Q
from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def space_info(request):
    return render(request, 'space_info.html')


def asteroids_explorer(request):
    # Get filter parameters from the request
    is_potentially_hazardous = request.GET.get('is_potentially_hazardous', 'false').lower() == 'true'
    is_sentry_object = request.GET.get('is_sentry_object', 'false').lower() == 'true'
    diameter = request.GET.get('diameter', None)
    type_id = request.GET.get('type_id', None)
    magnitude = request.GET.get('magnitude', None)
    year = request.GET.get('year', None)
    quarter = request.GET.get('quarter', None)
    month = request.GET.get('month', None)
    week = request.GET.get('week', None)
    day = request.GET.get('day', None)

    # Build the query based on the filter parameters
    filters = Q()
    filters &= Q(asteroid_id__is_potentially_hazardous=is_potentially_hazardous)
    filters &= Q(asteroid_id__is_sentry_object=is_sentry_object)
    if diameter is not None:
        filters &= Q(diameter_id__kilometer=diameter)
    if type_id is not None:
        filters &= Q(type_id=type_id)
    if magnitude is not None:
        filters &= Q(magnitude_id__magnitude=magnitude)
    if year is not None:
        filters &= Q(time_id__year=year)
    if quarter is not None:
        filters &= Q(time_id__quarter=quarter)
    if month is not None:
        filters &= Q(time_id__month=month)
    if week is not None:
        filters &= Q(time_id__week=week)
    if day is not None:
        filters &= Q(time_id__day=day)

    asteroids = (
        NeoSheet.objects.using('neo')
        .filter(filters)
        .values('asteroid_id')  # Group by asteroid_id
        .annotate(
            name=F('asteroid_name'),
            type_name=F('type_id__type_name'),
            type_description=F('type_id__description'),
        )
        .distinct('asteroid_id')
    )

    asteroids_data = []
    min_distance = float('inf')

    for asteroid in asteroids:
        asteroid_obj = Asteroid.objects.using('neo').get(asteroid_id=asteroid['asteroid_id'])
        asteroid['position'] = calculate_current_orbit(asteroid_obj)
        distance_squared = sum(coord ** 2 for coord in asteroid['position'])
        distance = (distance_squared ** 0.5).value

        if distance < min_distance:
            min_distance = distance

        asteroid_data = {
            'name': asteroid['name'],
            'type': asteroid['type_name'],
            'type_desc': asteroid['type_description'],
            'position': tuple(q.value for q in asteroid['position']),
            'close': get_closest_approach(asteroid_obj.asteroid_id)
        }
        asteroids_data.append(asteroid_data)

    return render(request, 'asteroids_explorer.html', {'asteroids': json.dumps(asteroids_data),
                                                       'factor': min_distance
                                                       })


def weather_info(request):
    # Assuming you have a FactSheet model with space weather data
    weather_dataset = WeatherSheet.objects.using('weather').all()
    unique_times = set()
    solar_wind_mag_data = []

    for weather in weather_dataset:
        time = str(weather.time.year) + '-' + str(weather.time.month).zfill(2) + '-' + str(weather.time.day).zfill(2) \
               + 'T' + str(weather.time.hour) + ':' + str(weather.time.minute)

        if time not in unique_times and not weather.mag.bx_gsm.is_nan():
            solar_wind_mag_data.append({
                'time': time,
                'bx_gsm': float(weather.mag.bx_gsm),
                'by_gsm': float(weather.mag.by_gsm),
                'bz_gsm': float(weather.mag.bz_gsm),
            })
            unique_times.add(time)

    # future_predictions = forecasting.forecast_solar_wind(space_weather_data)

    return render(request, 'weather.html', {
        'solar_wind_mag': json.dumps(solar_wind_mag_data),
        # 'future_predictions': future_predictions,
    })


def news_collection(request):
    news_data, news_data_word = WordCloudGenerator().process_news()
    return render(request, 'news.html', {'news_data': news_data, 'news_data_word': news_data_word})

