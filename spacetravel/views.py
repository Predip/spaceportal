import json
from .functions.asteroids.orbit_position import calculate_current_orbit
from .functions.wordcloud_generator import WordCloudGenerator
from spacetravel.models.neo import FactSheet
from spacetravel.models.news import News
from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def space_info(request):
    return render(request, 'space_info.html')


def asteroids_explorer(request):
    asteroids = FactSheet.objects.using('neo').all()

    asteroids_data = [
        {'name': asteroid.name, 'position': tuple(q.value for q in calculate_current_orbit(asteroid.asteroid_id))}
        for asteroid in asteroids
    ]

    return render(request, 'asteroids_explorer.html', {'asteroids': json.dumps(asteroids_data)})


def weather(request):
    return render(request, 'weather.html')


def news_collection(request):
    news_data = News.objects.using('news').all()
    news_data, news_data_word = WordCloudGenerator().process_news()
    return render(request, 'news.html', {'news_data': news_data, 'news_data_word': news_data_word})


def news_details(request, news_id):
    news = News.objects.get(id=news_id)
    return render(request, 'news/details.html', {'news': news})

