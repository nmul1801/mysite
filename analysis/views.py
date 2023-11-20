from django.shortcuts import render
from espn_api.football import League
import plotly.express as px
import pandas as pd

def index(request):
    league = League(league_id=64612107, year=2023, espn_s2='AECM85hbXZD%2FFG9s2ALIuE4XrHUPYodyji1oDVpO17ISfafgY9b9kxJ4QZaG1FiR1nVU0UW%2FtIQoPvtOfxxlA2y9xKn4dFzG1FO%2BNdP6ZsZZNly5BCtfCznME5sc8OJhBcY7nEjYRQ6b6tAtQvXYyvV65Ya6Hk4klxd0iIBzk6S82ZZiob5i8%2BThUSpeh0sUypUA%2FdpC06ZhaEVy9B0qVL%2B3tL8T3pK44imaNmSCGrLEmtTb5xmhmKIQYPPmE99IEvNy9ltr9DfPmJucfiPMVAfBcWaZUpEAE160r4SsIszqsw%3D%3D', swid='F71F32C4-9869-4DFB-A620-ADD15AA67520')
    # league = League(league_id=1927423163, year=2023, espn_s2='AECM85hbXZD%2FFG9s2ALIuE4XrHUPYodyji1oDVpO17ISfafgY9b9kxJ4QZaG1FiR1nVU0UW%2FtIQoPvtOfxxlA2y9xKn4dFzG1FO%2BNdP6ZsZZNly5BCtfCznME5sc8OJhBcY7nEjYRQ6b6tAtQvXYyvV65Ya6Hk4klxd0iIBzk6S82ZZiob5i8%2BThUSpeh0sUypUA%2FdpC06ZhaEVy9B0qVL%2B3tL8T3pK44imaNmSCGrLEmtTb5xmhmKIQYPPmE99IEvNy9ltr9DfPmJucfiPMVAfBcWaZUpEAE160r4SsIszqsw%3D%3D', swid='F71F32C4-9869-4DFB-A620-ADD15AA67520')

    total_opp_rank_dic = {}
    for team in league.teams:
        total_opp_rank_dic[team.team_id] = {"team_name" : team.team_name, "opp_rank_list" : list(), "opp_rank_sum": 0}

    num_weeks = 7

    for i in range(1, num_weeks + 1):
        box_scores = league.box_scores(week=i)
        id_score_arr = list()

        for box_score in box_scores:
            id_score_arr.append((box_score.home_team.team_id, box_score.home_score))
            id_score_arr.append((box_score.away_team.team_id, box_score.away_score))
            
        id_score_arr.sort(key=lambda team: team[1])

        ranking_dic = {}
        for i, scores in enumerate(id_score_arr):
            ranking_dic[scores[0]] = i + 1

        for box_score in box_scores:
            total_opp_rank_dic[box_score.home_team.team_id]["opp_rank_list"].append(ranking_dic[box_score.away_team.team_id])
            total_opp_rank_dic[box_score.away_team.team_id]["opp_rank_list"].append(ranking_dic[box_score.home_team.team_id])
        
    # view data
    all_team_opp_rank_list = list()
    for key in total_opp_rank_dic:
        (name, opp_rank_arr) = total_opp_rank_dic[key]["team_name"], total_opp_rank_dic[key]["opp_rank_list"]
        all_team_opp_rank_list.append((name, opp_rank_arr))

    all_team_opp_rank_list.sort(key=lambda team: sum(team[1]), reverse=True)

    all_scores_matrix = []
    for i in range(num_weeks):
        for team in all_team_opp_rank_list:
            new_score = [team[0], "Week " + str(i + 1), team[1][i]]
            all_scores_matrix.append(new_score)

    df_columns = ["Team", "Week", "BI"]

    df = pd.DataFrame(all_scores_matrix, columns=df_columns)

    fig = px.bar(df, x="Team", y="BI", color="Week", title="BI")
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)
        
    context = {
            'random': 0,
            'graph': graph
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


