from django.shortcuts import render
from espn_api.football import League
import requests
import analysis.analysisfuncs as analysisfuncs


def index(request):
    # league = League(league_id=64612107, year=2023, espn_s2='AECM85hbXZD%2FFG9s2ALIuE4XrHUPYodyji1oDVpO17ISfafgY9b9kxJ4QZaG1FiR1nVU0UW%2FtIQoPvtOfxxlA2y9xKn4dFzG1FO%2BNdP6ZsZZNly5BCtfCznME5sc8OJhBcY7nEjYRQ6b6tAtQvXYyvV65Ya6Hk4klxd0iIBzk6S82ZZiob5i8%2BThUSpeh0sUypUA%2FdpC06ZhaEVy9B0qVL%2B3tL8T3pK44imaNmSCGrLEmtTb5xmhmKIQYPPmE99IEvNy9ltr9DfPmJucfiPMVAfBcWaZUpEAE160r4SsIszqsw%3D%3D', swid='F71F32C4-9869-4DFB-A620-ADD15AA67520')
    # league = League(league_id=1927423163, year=2023, espn_s2='AECM85hbXZD%2FFG9s2ALIuE4XrHUPYodyji1oDVpO17ISfafgY9b9kxJ4QZaG1FiR1nVU0UW%2FtIQoPvtOfxxlA2y9xKn4dFzG1FO%2BNdP6ZsZZNly5BCtfCznME5sc8OJhBcY7nEjYRQ6b6tAtQvXYyvV65Ya6Hk4klxd0iIBzk6S82ZZiob5i8%2BThUSpeh0sUypUA%2FdpC06ZhaEVy9B0qVL%2B3tL8T3pK44imaNmSCGrLEmtTb5xmhmKIQYPPmE99IEvNy9ltr9DfPmJucfiPMVAfBcWaZUpEAE160r4SsIszqsw%3D%3D', swid='F71F32C4-9869-4DFB-A620-ADD15AA67520')
    return render(request, 'index.html', context={'error_code': 0})


def analysis(request):
    plat = request.GET.get('platform', 'espn')
    league_id = request.GET.get('id', '')
    if plat == 'espn':
        s2 = request.GET.get('s2', '')
        swid = request.GET.get('swid', '')

    if plat == 'espn':
        try: 
            league = League(league_id=league_id, year=2023, espn_s2=s2, swid=swid)
        except Exception as e:
            return render(request, 'index.html', context={'error_code': 1})
        team_dic, num_weeks = analysisfuncs.construct_team_dic(league)
    else:
        # try to get response, error if none
        r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id) + "/rosters")
        if r.status_code != 200:
            return render(request, 'index.html', context={'error_code': 1})
        team_dic, num_weeks = analysisfuncs.construct_team_dic_sleeper(league_id)

    ew_graph = analysisfuncs.get_expected_wins_graph(team_dic, num_weeks)
    ew_diff_graph = analysisfuncs.get_ew_difference_graph(team_dic)
    luck_graph = analysisfuncs.get_luck_graph(team_dic, num_weeks)
    bi_graph = analysisfuncs.get_bonage_graph(team_dic, num_weeks)
    consistency_graph = analysisfuncs.get_consistency_graph(team_dic)
        
    context = {
            'random': 0,
            'exp_wins_g': ew_graph,
            'ew_diff_g': ew_diff_graph,
            'luck_g': luck_graph,
            'bi_g': bi_graph,
            'consistency_g': consistency_graph
    }

    return render(request, 'analysis.html', context=context)

