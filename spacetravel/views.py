import json
from .functions.neo.orbit_position import calculate_current_orbit, get_closest_approach
from .functions.news.wordcloud_generator import get_wordcloud_data
# from .functions.weather import forecasting
from .models import Asteroid, NeoSheet, WeatherSheet, NewsSheet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    weather_dataset = WeatherSheet.objects.using('weather').all()
    unique_times = set()
    mag_data = []
    plasma = []
    magnetometer = []
    proton = []

    for weather in weather_dataset:
        time = str(weather.time.year) + '-' + str(weather.time.month).zfill(2) + '-' + str(weather.time.day).zfill(2) \
               + 'T' + str(weather.time.hour) + ':' + str(weather.time.minute)

        if time not in unique_times and not weather.mag.bx_gsm.is_nan():
            mag_data.append({
                'time': time,
                'bx_gsm': float(weather.mag.bx_gsm),
                'by_gsm': float(weather.mag.by_gsm),
                'bz_gsm': float(weather.mag.bz_gsm),
            })

            if time not in unique_times and not weather.plasma.density.is_nan():
                plasma.append({
                    'time': time,
                    'density': float(weather.plasma.density),
                    'speed': float(weather.plasma.speed),
                })

            if time not in unique_times and not weather.magnetometer.he.is_nan():
                magnetometer.append({
                    'time': time,
                    'he': float(weather.magnetometer.he),
                    'hp': float(weather.magnetometer.hp),
                    'hn': float(weather.magnetometer.hn),
                    'total': float(weather.magnetometer.total),
                })

            if time not in unique_times and not weather.proton.energy.is_nan():
                proton.append({
                    'time': time,
                    'energy': float(weather.proton.energy),
                    'flux': float(weather.proton.flux),
                })
            unique_times.add(time)

    # future_predictions = forecasting.forecast_solar_wind(space_weather_data)
    final_protons = {}
    energy_counts = {}
    for entry in proton:
        energy = entry['energy']
        energy_counts[energy] = energy_counts.get(energy, 0) + 1

    # Select unique values that appear more than twice
    selected_energy_levels = [energy for energy, count in energy_counts.items() if count > 2]

    selected_protons = [{'time': entry['time'], 'energy': entry['energy'], 'flux': entry['flux']} for entry in
                        proton if entry['energy'] in selected_energy_levels]

    # Group data by 'energy' and prepare for JSON serialization
    for energy_level in selected_energy_levels:
        group = [{'time': entry['time'], 'flux': entry['flux']} for entry in selected_protons if
                 entry['energy'] == energy_level]
        group.sort(key=lambda x: x['time'])
        print(f"Sorted group for {energy_level}: {group}")
        final_protons[energy_level] = group

    return render(request, 'weather.html', {
        'mag': json.dumps(mag_data),
        'plasma': json.dumps(plasma),
        'magnetometer': json.dumps(magnetometer),
        'proton': final_protons,
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
