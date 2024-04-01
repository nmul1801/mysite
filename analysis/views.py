from django.shortcuts import render
from analysis.league.league import League


def index(request):
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

    ew_graph = analysis_league.get_expected_wins_graph()
    ew_team_dic, ew_diff_graph = analysis_league.get_ew_difference_graph()
    luck_dic, luck_graph = analysis_league.get_luck_graph()
    bi_graph = analysis_league.get_bonage_graph()
    consistency_graph = analysis_league.get_consistency_graph()
    sleepers_dict = analysis_league.get_sleepers()
    league_pos_rank = analysis_league.get_pos_rank_through_draft_graph()
    first_half_pos_rank = analysis_league.get_average_pos_rank_graph(half=1)
    second_half_pos_rank = analysis_league.get_average_pos_rank_graph(half=2)
    draft_round_dict = analysis_league.get_draft_injury_table()
    prob_auc_g = analysis_league.get_probdcurve()
    

    context = {
            'num_weeks': analysis_league.num_weeks,
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
            'teams_list': [t.get_name() for t in analysis_league.teams.values()],
            'ew_dic': ew_team_dic,
            'luck_dic': luck_dic,
            'prob_auc_g': prob_auc_g
    }

    return render(request, 'analysis.html', context=context)

