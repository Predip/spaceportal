from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def space_info(request):
    return render(request, 'space_info.html')


def asteroids_explorer(request):
    return render(request, 'asteroids_explorer.html')


def weather(request):
    return render(request, 'weather.html')


def news_collection(request):
    return render(request, 'news.html')
