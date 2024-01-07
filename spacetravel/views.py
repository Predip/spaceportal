import json
# from .functions.weather import forecasting
from collections import defaultdict
from datetime import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Q
from django.shortcuts import render

from .functions.neo.orbit_position import calculate_current_orbit, get_closest_approach
from .functions.news.wordcloud_generator import get_wordcloud_data
from .models import Asteroid, NeoSheet, WeatherSheet, NewsSheet


def format_time(time):
    return f"{time['time__year']}-{str(time['time__month']).zfill(2)}-{str(time['time__day']).zfill(2)}" \
           f"T{time['time__hour']}:{str(time['time__minute'])}"


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
    weather_dataset = WeatherSheet.objects.using('weather') \
        .select_related('time', 'mag', 'plasma', 'magnetometer', 'proton').values(
        'time__year', 'time__month', 'time__day', 'time__hour', 'time__minute',
        'mag__bx_gsm', 'mag__by_gsm', 'mag__bz_gsm',
        'plasma__density', 'plasma__speed',
        'magnetometer__he', 'magnetometer__hp', 'magnetometer__hn', 'magnetometer__total',
        'proton__energy', 'proton__flux'
    )
    unique_times = set()
    mag_data = []
    plasma_data = []
    magnetometer_data = []
    proton_data = []

    print(weather_dataset)
    counter = 0
    for weather in weather_dataset:
        time = format_time(weather)

        if time not in unique_times:
            unique_times.add(time)
            print(counter)
            print(datetime.now())

            if weather['mag__bx_gsm'] is not None:
                mag_data.append({
                    'time': time,
                    'bx_gsm': float(weather['mag__bx_gsm']),
                    'by_gsm': float(weather['mag__by_gsm']),
                    'bz_gsm': float(weather['mag__bz_gsm']),
                })

            if weather['plasma__density'] is not None and weather['plasma__speed'] is not None:
                plasma_data.append({
                    'time': time,
                    'density': float(weather['plasma__density']),
                    'speed': float(weather['plasma__speed']),
                })

            if weather['magnetometer__he'] is not None:
                magnetometer_data.append({
                    'time': time,
                    'he': float(weather['magnetometer__he']),
                    'hp': float(weather['magnetometer__hp']),
                    'hn': float(weather['magnetometer__hn']),
                    'total': float(weather['magnetometer__total']),
                })

            if weather['proton__energy'] is not None:
                proton_data.append({
                    'time': time,
                    'energy': float(weather['proton__energy']),
                    'flux': float(weather['proton__flux']),
                })
            print("---------------------------------------")
            counter += 1

    # future_predictions = forecasting.forecast_solar_wind(space_weather_data)
    final_protons = defaultdict(list)

    for entry in proton_data:
        final_protons[entry['energy']].append({'time': entry['time'], 'flux': entry['flux']})

    # Select unique values that appear more than twice
    selected_energy_levels = [energy for energy, count in final_protons.items() if len(count) > 2]

    # Group data by 'energy' and prepare for JSON serialization
    for energy_level in selected_energy_levels:
        final_protons[energy_level].sort(key=lambda x: x['time'])

    return render(request, 'weather.html', {
        'mag': json.dumps(mag_data),
        'plasma': json.dumps(plasma_data),
        'magnetometer': json.dumps(magnetometer_data),
        'proton': dict(final_protons),
        # 'future_predictions': future_predictions,
    })


def news_collection(request):
    news_dataset = NewsSheet.objects.using('news').order_by('time_id').all()
    paginator = Paginator(news_dataset, 10)
    page = request.GET.get('page', 1)

    try:
        current_page_data = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        current_page_data = paginator.page(1)

    news_data = []

    for news in current_page_data:
        time = str(news.time_id.year) + '-' + str(news.time_id.month).zfill(2) + '-' + str(news.time_id.day).zfill(2) \
               + 'T' + str(news.time_id.hour).zfill(2) + ':' + str(news.time_id.minute).zfill(2)

        news_data.append({
            'title': news.news_id.title,
            'summary': news.news_id.summary,
            'category': news.category_id.category_name,
            'news_site': news.source_id.source_name,
            'sentiment': float(news.sentiment_id.score),
            'time': time,
            'url': news.news_id.url,
            'img_url': news.news_id.img_url,
        })

    news_data_word = get_wordcloud_data(news_dataset)

    return render(request, 'news.html', {
        'news_data': json.dumps(news_data), 'news_data_word': news_data_word,
        'has_next': current_page_data.has_next(), 'has_previous': current_page_data.has_previous(),
        'next_page': current_page_data.next_page_number, 'previous_page': current_page_data.previous_page_number,
        'current_page': current_page_data.number, 'total_page': current_page_data.paginator.num_pages,
    })
