import time

import requests
import json
from django.db.models import Count
from django.core import serializers
from .models import SeasonFilter, SeasonWin, SeasonGoal, SeasonShots
from django.db import connection
from scipy.stats import rankdata

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC

def add_season():
    SeasonFilter.objects.all().delete()
    response = requests.get(
        f"https://footballapi.pulselive.com/football/competitions/1/compseasons?page=0&pageSize=100",
        headers={
            "origin": "https://www.premierleague.com"
        }
    )

    data = json.loads(response.text)

    for season in data['content']:
        myseason = SeasonFilter(season=season['label'],
                                dataindex=season['id'],
                                data='')
        myseason.save()
    return data

def add_win():
    SeasonWin.objects.all().delete()
    m_season = SeasonFilter.objects.all()

    data = []
    for season_data in m_season:
        response = requests.get(
            f"https://footballapi.pulselive.com/football/stats/ranked/teams/wins?page=0&pageSize=20&compSeasons={season_data.dataindex}&comps=1&altIds=true",
            headers={
                "origin": "https://www.premierleague.com"
            }
        )
        response = json.loads(response.text)
        content = response['stats']['content']
        for team in content:
            # print(season_data.season + ' team:___ ' + team['owner']['name'] + ' value:___ ' + team['value'])
            txt = 'season: {}  club: {}  value: {}'
            # print(txt.format(season_data.season, team['owner']['name'], team['value']))
            myclubs = SeasonWin(dataindex=season_data.dataindex,
                                club=team['owner']['name'],
                                win=team['value'],
                                season=season_data.season)
            myclubs.save()

        data.extend(content)
        # for res in response['states']['content']:
        #     print(res['value'])
        # data += response.text
    m_season = SeasonFilter.objects.all()

    return data

def add_goal():
    SeasonGoal.objects.all().delete()
    m_season = SeasonFilter.objects.all()

    data = []
    for season_data in m_season:
        response = requests.get(
            f"https://footballapi.pulselive.com/football/stats/ranked/teams/goals?page=0&pageSize=20&compSeasons={season_data.dataindex}&comps=1&altIds=true",
            headers={
                "origin": "https://www.premierleague.com"
            }
        )
        response = json.loads(response.text)
        content = response['stats']['content']
        for team in content:
            # print(season_data.season + ' team:___ ' + team['owner']['name'] + ' value:___ ' + team['value'])
            txt = 'season: {}  club: {}  value: {}'
            # print(txt.format(season_data.season, team['owner']['name'], team['value']))
            myclubs = SeasonGoal(dataindex=season_data.dataindex,
                                club=team['owner']['name'],
                                goal=team['value'],
                                season=season_data.season)
            myclubs.save()

        data.extend(content)
        # for res in response['states']['content']:
        #     print(res['value'])
        # data += response.text
    m_season = SeasonFilter.objects.all()

    return data

def add_shots():
    SeasonShots.objects.all().delete()
    m_season = SeasonFilter.objects.all()

    data = []
    for season_data in m_season:
        response = requests.get(
            f"https://footballapi.pulselive.com/football/stats/ranked/teams/total_scoring_att?page=0&pageSize=20&compSeasons={season_data.dataindex}&comps=1&altIds=true",
            headers={
                "origin": "https://www.premierleague.com"
            }
        )
        response = json.loads(response.text)
        content = response['stats']['content']
        for team in content:
            # print(season_data.season + ' team:___ ' + team['owner']['name'] + ' value:___ ' + team['value'])
            txt = 'season: {}  club: {}  value: {}'
            # print(txt.format(season_data.season, team['owner']['name'], team['value']))
            myclubs = SeasonShots(dataindex=season_data.dataindex,
                                club=team['owner']['name'],
                                shots=team['value'],
                                season=season_data.season)
            myclubs.save()

        data.extend(content)
        # for res in response['states']['content']:
        #     print(res['value'])
        # data += response.text
    m_season = SeasonFilter.objects.all()

    return data

def get_win():
    team_win = SeasonWin.objects.values('club').annotate(total=Count('club')).order_by()
    win_season = []
    for club in team_win:
        club_win = SeasonWin.objects.filter(club=club['club']).order_by("dataindex")
        qs_json = serializers.serialize('json', club_win)
        win_season.extend(club_win.values())
    year_season = SeasonFilter.objects.all().values('season')
    print(team_win)
    data = {
        'win': list(win_season),
        'year': list(year_season),
        'club': list(team_win)
    }
    winData = json.dumps(data)
    return winData

def get_goal():
    team_goal = SeasonGoal.objects.values('club').annotate(total=Count('club')).order_by()
    goal_season = []
    for club in team_goal:
        club_goal = SeasonGoal.objects.filter(club=club['club']).order_by("dataindex")
        qs_json = serializers.serialize('json', club_goal)
        goal_season.extend(club_goal.values())
    year_season = SeasonFilter.objects.all().values('season')

    data = {
        'goal': list(goal_season),
        'year': list(year_season),
        'club': list(team_goal)
    }
    goalData = json.dumps(data)
    return goalData

def get_shots():
    team_shots = SeasonShots.objects.values('club').annotate(total=Count('club')).order_by()
    shots_season = []
    for club in team_shots:
        club_shots = SeasonShots.objects.filter(club=club['club']).order_by("dataindex")
        qs_json = serializers.serialize('json', club_shots)
        shots_season.extend(club_shots.values())
    year_season = SeasonFilter.objects.all().values('season')

    data = {
        'shots': list(shots_season),
        'year': list(year_season),
        'club': list(team_shots)
    }
    shotsData = json.dumps(data)
    return shotsData

def predict():
    team = SeasonWin.objects.values('club').annotate(total=Count('club')).order_by()

    team_win = SeasonWin.objects.all()
    team_shot = SeasonShots.objects.all()
    team_goal = SeasonGoal.objects.all()
    with connection.cursor() as cursor:
        cursor.execute('SELECT club,GROUP_CONCAT(win ORDER BY season ASC SEPARATOR " ") AS calc_win  FROM sportapp_seasonwin GROUP BY club')
        row = cursor.fetchall()
    all_json = []
    m_club_win = []
    m_club = []
    m_win = []
    m_team = []
    for club in row:
        text = club[1].split(' ')
        if len(text) > 6:
            m_team.append(club[0])
            X = np.arange(len(text)).reshape(-1, 1)
            y = np.array(text).reshape(-1, 1)
            to_predict_x = np.arange(len(text), len(text)+10, 1).reshape(-1, 1)
            #
            regsr = LinearRegression()
            regsr.fit(X, y, )
            # #
            predicted_y = regsr.predict(to_predict_x)
            m_club_win.append(predicted_y)
    m_club_win = np.array(m_club_win)
    for i in range(m_club_win.shape[1]):
        m_club.append(m_club_win[0:m_club_win.shape[0], i])

    # rd = rankdata(m_club[0], method='min')
    # final_data = []
    # for i in range(len(rd)):
    #     data = {
    #         'club': m_team[i],
    #         'win': rd[i]
    #     }
    #     final_data.append(data)
    # final_data = sorted(final_data, key=lambda i: i['win'], reverse=True)
    # final_team = []
    # for i in final_data:
    #     final_team.append(i['club'])
    # final_team = json.dumps({
    #     'team': list(final_team)
    # })
    all_team = []
    print('all_team')
    for i in range(len(m_club)):
        final_data = []
        rd = rankdata(m_club[i], method='min')
        for j in range(len(rd)):
            data = {
                'club': m_team[j],
                'win': int(rd[j])
            }
            final_data.append(data)
        final_data = sorted(final_data, key=lambda k: k['win'], reverse=True)

        all_team.append(final_data)
    print(list(all_team))
    all_team = json.dumps(all_team)
    return all_team

def send_data_per_club(req):
    global data
    m_club = req['club']
    req_type = req['type']
    if req_type == 'win':
        data = SeasonWin.objects.filter(club=m_club).order_by('dataindex').values()
    if req_type == 'goal':
        data = SeasonGoal.objects.filter(club=m_club).order_by('dataindex').values()
    if req_type == 'shots':
        data = SeasonShots.objects.filter(club=m_club).order_by('dataindex').values()
    final_data = json.dumps({
        'club': m_club,
        'clubdata': list(data)
    })
    return final_data