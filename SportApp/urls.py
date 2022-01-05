from django.urls import path
from .views import News, WinScrape, GoalScrape, ShotsScrape, WinView, GoalView, ShotsView, WinPredict, Club

urlpatterns = [
    path('', News, name='news'),
    path('winScrape/', WinScrape, name='WinScrape'),
    path('goalScrape/', GoalScrape, name='GoalScrape'),
    path('shotsScrape/', ShotsScrape, name='ShotsScrape'),
    path('winView/', WinView, name='WinView'),
    path('goalView/', GoalView, name='GoalView'),
    path('shotsView/', ShotsView, name='ShotsView'),
    path('predict/', WinPredict, name='Predict'),
    path('club/', Club, name='Club')
]