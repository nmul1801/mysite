from django.shortcuts import render
from analysis.league.league import League


def index(request):
    # league = League(league_id=64612107, year=2023, espn_s2='AECM85hbXZD%2FFG9s2ALIuE4XrHUPYodyji1oDVpO17ISfafgY9b9kxJ4QZaG1FiR1nVU0UW%2FtIQoPvtOfxxlA2y9xKn4dFzG1FO%2BNdP6ZsZZNly5BCtfCznME5sc8OJhBcY7nEjYRQ6b6tAtQvXYyvV65Ya6Hk4klxd0iIBzk6S82ZZiob5i8%2BThUSpeh0sUypUA%2FdpC06ZhaEVy9B0qVL%2B3tL8T3pK44imaNmSCGrLEmtTb5xmhmKIQYPPmE99IEvNy9ltr9DfPmJucfiPMVAfBcWaZUpEAE160r4SsIszqsw%3D%3D', swid='F71F32C4-9869-4DFB-A620-ADD15AA67520')
    # league = League(league_id=1927423163, year=2023, espn_s2='AECM85hbXZD%2FFG9s2ALIuE4XrHUPYodyji1oDVpO17ISfafgY9b9kxJ4QZaG1FiR1nVU0UW%2FtIQoPvtOfxxlA2y9xKn4dFzG1FO%2BNdP6ZsZZNly5BCtfCznME5sc8OJhBcY7nEjYRQ6b6tAtQvXYyvV65Ya6Hk4klxd0iIBzk6S82ZZiob5i8%2BThUSpeh0sUypUA%2FdpC06ZhaEVy9B0qVL%2B3tL8T3pK44imaNmSCGrLEmtTb5xmhmKIQYPPmE99IEvNy9ltr9DfPmJucfiPMVAfBcWaZUpEAE160r4SsIszqsw%3D%3D', swid='F71F32C4-9869-4DFB-A620-ADD15AA67520')
    return render(request, 'index.html', context={'error_code': 0})


def analysis(request):
    # needed info
    plat = request.GET.get('platform', 'espn')
    league_id = request.GET.get('id', '')
    s2, swid = None, None

    # only needed for espn
    if plat == 'espn':
        s2 = request.GET.get('s2', '')
        swid = request.GET.get('swid', '')

    analysis_league = League(plat, league_id, s2=s2, swid=swid)
    

    # team_dic, num_weeks = analysisfuncs.construct_team_dic(team_dic, num_weeks)

    # ew_graph = analysisfuncs.get_expected_wins_graph(team_dic, num_weeks)
    # ew_diff_graph = analysisfuncs.get_ew_difference_graph(team_dic)
    # luck_graph = analysisfuncs.get_luck_graph(team_dic, num_weeks)
    # bi_graph = analysisfuncs.get_bonage_graph(team_dic, num_weeks)
    # consistency_graph = analysisfuncs.get_consistency_graph(team_dic)

    ew_graph = analysis_league.get_expected_wins_graph()
    ew_diff_graph = analysis_league.get_ew_difference_graph()
    luck_graph = analysis_league.get_luck_graph()
    bi_graph = analysis_league.get_bonage_graph()
    consistency_graph = analysis_league.get_consistency_graph()
    sleepers_dict = analysis_league.get_sleepers()
    league_pos_rank = analysis_league.get_pos_rank_through_draft_graph()
    first_half_pos_rank = analysis_league.get_average_pos_rank_graph(half=1)
    second_half_pos_rank = analysis_league.get_average_pos_rank_graph(half=2)
    draft_round_dict = analysis_league.get_draft_injury_table()


    context = {
            'random': 0,
            'exp_wins_g': ew_graph,
            'ew_diff_g': ew_diff_graph,
            'luck_g': luck_graph,
            'bi_g': bi_graph,
            'consistency_g': consistency_graph,
            'sleepers_dict_items': list(sleepers_dict.items()),
            'league_pos_rank': league_pos_rank,
            'first_half_pos_rank': first_half_pos_rank,
            'second_half_pos_rank': second_half_pos_rank,
            'draft_round_dict': draft_round_dict,
            'teams_list': [t.get_name() for t in analysis_league.teams.values()]
    }

    return render(request, 'analysis.html', context=context)

