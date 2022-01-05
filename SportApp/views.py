from django.shortcuts import render
from django.shortcuts import HttpResponse
from .engine import add_season, add_win, get_win, add_goal, add_shots, get_goal, get_shots, predict, send_data_per_club

# Create your views here.

def News(request):
    add_season()

    context = {
        'data': get_win()
    }
    return render(request ,'home.html', context)

def WinScrape(request):
    return HttpResponse(add_win())

def GoalScrape(request):
    return HttpResponse(add_goal())

def ShotsScrape(request):
    return HttpResponse(add_shots())

def WinView(request):
    return HttpResponse(get_win())

def GoalView(request):
    return HttpResponse(get_goal())

def ShotsView(request):
    return HttpResponse(get_shots())

def WinPredict(request):
    return HttpResponse(predict())

def Club(request):
    print(request.GET)
    return HttpResponse(send_data_per_club(request.GET))