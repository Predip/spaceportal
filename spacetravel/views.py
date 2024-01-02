import json
from .functions.asteroids.orbit_position import calculate_current_orbit
from .functions.wordcloud_generator import WordCloudGenerator
from spacetravel.models.neo import FactSheet
from spacetravel.models.news import News
from django.db.models import Q
from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def space_info(request):
    return render(request, 'space_info.html')


def asteroids_explorer(request):
    # Get filter parameters from the request
    is_potentially_hazardous = request.GET.get('is_potentially_hazardous', False)
    is_sentry_object = request.GET.get('is_sentry_object', False)
    diameter = request.GET.get('diameter', None)
    type_id = request.GET.get('type_id', None)
    magnitude = request.GET.get('magnitude', None)
    year = request.GET.get('year', None)
    quarter = request.GET.get('quarter', None)
    month = request.GET.get('month', None)
    week = request.GET.get('week', None)
    day = request.GET.get('day', None)
    hour = request.GET.get('hour', None)
    minute = request.GET.get('minute', None)

    # Convert string values to boolean
    is_potentially_hazardous = is_potentially_hazardous.lower() == 'true' if is_potentially_hazardous else False
    is_sentry_object = is_sentry_object.lower() == 'true' if is_sentry_object else False

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
    if hour is not None:
        filters &= Q(time_id__hour=hour)
    if minute is not None:
        filters &= Q(time_id__minute=minute)

    asteroids = FactSheet.objects.using('neo').filter(filters)

    # Calculate max and min distances
    min_distance = float('inf')

    for asteroid in asteroids:
        position = calculate_current_orbit(asteroid.asteroid_id)
        distance = ((position[0] ** 2 + position[1] ** 2 + position[2] ** 2) ** 0.5).value

        if distance < min_distance:
            min_distance = distance

    asteroids_data = [
        {
            'name': asteroid.name,
            'position': tuple(q.value for q in calculate_current_orbit(asteroid.asteroid_id))
        }
        for asteroid in asteroids
    ]

    return render(request, 'asteroids_explorer.html', {'asteroids': json.dumps(asteroids_data),
                                                       'factor': min_distance
                                                       })


def weather(request):
    return render(request, 'weather.html')


def news_collection(request):
    news_data = News.objects.using('news').all()
    news_data, news_data_word = WordCloudGenerator().process_news()
    return render(request, 'news.html', {'news_data': news_data, 'news_data_word': news_data_word})


def news_details(request, news_id):
    news = News.objects.get(id=news_id)
    return render(request, 'news/details.html', {'news': news})
