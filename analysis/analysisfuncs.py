import pandas as pd
import math
import plotly.express as px
from scipy.stats import norm
import statistics
import requests
import json

# sleeper team dictionary construction
def construct_team_dic_sleeper(league_id):

    num_weeks = get_num_weeks_sleeper(league_id)
    
    r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id) + "/rosters")
    rosters_ob = json.loads(r.text)

    user_dic = {ros['owner_id']: {"roster_id": ros['roster_id']} for ros in rosters_ob}

    roster_dic = {ros['roster_id']: {"opp_rank_list" : list(), "rank_list" : list(), "ew_list": list(), "BI_list": list(), "score_list": list(), "win_list": list()} for ros in rosters_ob}

    for ros in rosters_ob:
        roster_dic[ros['roster_id']]['user_id'] = ros['owner_id']

    r = requests.get(url="https://api.sleeper.app/v1/league/988223204793614336/users")
    json_ob = json.loads(r.text)

    for team_ob in json_ob:
        cur_roster_num = user_dic[team_ob['user_id']]['roster_id']
        roster_dic[cur_roster_num]['team_name'] = team_ob['display_name']

    for i in range(1, num_weeks + 1):
        weekly_dic = {}
        r = requests.get(url="https://api.sleeper.app/v1/league/988223204793614336/matchups/" + str(i))
        matchup_ob = json.loads(r.text)

        for match_ob in matchup_ob:
            roster_dic[match_ob['roster_id']]['score_list'].append(match_ob['points'])
            weekly_dic[match_ob['roster_id']] = {'score': match_ob['points'], 'matchup_id': match_ob['matchup_id']}
        
        weekly_dic = dict(sorted(weekly_dic.items(), key=lambda item: item[1]['score'], reverse=True))
        matchup_dic = {}
        for r, k in enumerate(weekly_dic):
            rank = r + 1
            weekly_dic[k]['rank'] = rank
            cur_m_id = weekly_dic[k]['matchup_id']
            if cur_m_id in matchup_dic:
                other_team_dic = weekly_dic[matchup_dic[cur_m_id]]  

                weekly_dic[k]['opp_rank'] = other_team_dic['rank']
                other_team_dic['opp_rank'] = rank
                if weekly_dic[k]['score'] > other_team_dic['score']:
                    other_team_dic['win'] = 0
                    weekly_dic[k]['win'] = 1
                elif weekly_dic[k]['score'] < other_team_dic['score']:
                    other_team_dic['win'] = 1
                    weekly_dic[k]['win'] = 0
                else:
                    other_team_dic['win'] = 0.5
                    weekly_dic[k]['win'] = 0.5
                    
            else:
                matchup_dic[weekly_dic[k]['matchup_id']] = k

        for r in roster_dic:
            roster_dic[r]['rank_list'].append(weekly_dic[r]['rank'])
            roster_dic[r]['opp_rank_list'].append(weekly_dic[r]['opp_rank'])
            roster_dic[r]['win_list'].append(weekly_dic[r]['win'])
        
    for t in roster_dic:
        roster_dic[t]["BI_list"] = [len(roster_dic) - r + 1 for r in roster_dic[t]['opp_rank_list']]
        roster_dic[t]["ew_list"] = [round(r / len(roster_dic), 2) for r in roster_dic[t]['rank_list']]

    return roster_dic, num_weeks

def get_num_weeks_sleeper(league_id):
    r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id))
    league_ob = json.loads(r.text)
    p_start = league_ob['settings']['playoff_week_start']
    return min(get_cur_finished_nfl_week(), p_start - 1)

def create_rank_list(num_list):
    ranked_list = [1]
    cur_ranking = 1
    for i, cur_score in enumerate(num_list):
        if i == 0: continue
        if cur_score == num_list[i - 1]:
            ranked_list.append(ranked_list[-1])
        else:
            ranked_list.append(i + 1)
    return ranked_list

def get_ew_diff_list(master_dic):
    ew_diff_list = list()
    for key in master_dic:
        (name, ew_diff) = master_dic[key]["team_name"], sum(master_dic[key]["win_list"]) - sum(master_dic[key]["ew_list"])
        ew_diff_list.append((name, ew_diff))

    ew_diff_list.sort(key=lambda x: x[1], reverse=True)
    return ew_diff_list

def get_cur_finished_nfl_week():
    res_nfl = requests.get(url="https://api.sleeper.app/v1/state/nfl")
    nfl_ob = json.loads(res_nfl.text)
    return nfl_ob['week'] - 1

def construct_team_dic(league):
    cur_nfl_week = get_cur_finished_nfl_week()
    reg_szn_games = league.settings.reg_season_count
    num_weeks = min(reg_szn_games, cur_nfl_week)
    
    master_dic = {}
    for team in league.teams:
        master_dic[team.team_id] = {"team_name" : team.team_name, "opp_rank_list" : list(), "rank_list" : list(), "ew_list": list(), "BI_list": list(),"score_list" : team.scores}
        filtered_outcomes = list(map(lambda x: 1 if x == 'W' else 0, team.outcomes))
        master_dic[team.team_id]["win_list"] = filtered_outcomes

    # assemble ranking dic
    for i in range(num_weeks):
        # list of tuples, (id, weekly score)
        weekly_id_score_pairs = list()
        for key in master_dic:
            weekly_id_score_pairs.append((key, master_dic[key]["score_list"][i]))
        weekly_id_score_pairs.sort(key=lambda team: team[1], reverse=True)
        rank_list = create_rank_list(list(map(lambda x : x[1], weekly_id_score_pairs)))

        for i, tup in enumerate(weekly_id_score_pairs):
            master_dic[tup[0]]["rank_list"].append(rank_list[i])
            ew = (len(league.teams) - rank_list[i]) / (len(league.teams) - 1)
            master_dic[tup[0]]["ew_list"].append(round(ew, 2))


    for i in range(1, num_weeks + 1):
        box_scores = league.box_scores(week=i)

        for box_score in box_scores:
            home_id, away_id = box_score.home_team.team_id, box_score.away_team.team_id

            home_rank = master_dic[home_id]["rank_list"][i - 1]
            away_rank = master_dic[away_id]["rank_list"][i - 1]
            # opponent rank
            master_dic[home_id]["opp_rank_list"].append(away_rank)
            master_dic[away_id]["opp_rank_list"].append(home_rank)

            master_dic[home_id]["BI_list"].append(len(league.teams) - away_rank + 1)
            master_dic[away_id]["BI_list"].append(len(league.teams) - home_rank + 1)

    return master_dic, num_weeks

def get_expected_wins_graph(master_dic, num_weeks):
    all_team_list = list()
    for key in master_dic:
        (name, ew_list, win_list) = master_dic[key]["team_name"], master_dic[key]["ew_list"], master_dic[key]["win_list"]
        all_team_list.append((name, ew_list, win_list))

    all_team_list.sort(key=lambda team: sum(team[1]), reverse=True)

    all_wins_matrix = []
    for i in range(num_weeks):
        for team in all_team_list:
            new_ew = [team[0], "Week " + str(i + 1), team[1][i]]
            all_wins_matrix.append(new_ew)

            
    df_columns = ["Team", "Week", "Wins"]

    df = pd.DataFrame(all_wins_matrix, columns=df_columns)

    fig = px.bar(df, x="Team", y="Wins", color="Week", title="Expected Wins, Weekly")
    figHTML = fig.to_html(full_html=False)
    return figHTML

def get_ew_difference_graph(master_dic):
    ew_diff_list = get_ew_diff_list(master_dic)

    all_diff_matrix = []
    for team in ew_diff_list:
        new_ew = [team[0], team[1]]
        all_diff_matrix.append(new_ew)

    df_columns = ["Team", "EW Difference"]

    df = pd.DataFrame(all_diff_matrix, columns=df_columns)

    fig = px.bar(df, x="Team", y="EW Difference", title="Difference in Total Wins and Total Expected Wins")
    figHTML = fig.to_html(full_html=False)
    return figHTML

def get_luck_graph(master_dic, num_weeks):
    ew_diff_list = get_ew_diff_list(master_dic)

    n = num_weeks
    p = 0.5
    avg_ew = n * p
    variance = n * p * (1 - p)
    luck_P_list = list()
    luck_list = list()


    for team in ew_diff_list:
        z_score = team[1] / math.sqrt(variance)
        p = norm.cdf(z_score)
        luck = "Below Zero"
        if p > 0.5:
            p = 1 - p
            luck = "Above Zero"
        luck_P_list.append(round((p * 100), 2))
        luck_list.append(luck)

    luck_matrix = []
    for i, team in enumerate(ew_diff_list):
        new_luck = [team[0], luck_P_list[i], luck_list[i]]
        luck_matrix.append(new_luck)

    df_columns = ["Team", "Percent Odds of [W - E(W)] Occurring", "W - E(W)"]

    df = pd.DataFrame(luck_matrix, columns=df_columns)

    fig = px.bar(df, 
        x="Team", 
        y="Percent Odds of [W - E(W)] Occurring", 
        title="Odds of Each Team's [W - E(W)] Occurring",
        color='W - E(W)',
        color_discrete_map={
            'Above Zero': 'green',
            'Below Zero': 'red'
        })
    figHTML = fig.to_html(full_html=False)
    return figHTML

def get_bonage_graph(master_dic, num_weeks):
    all_team_list = list()
    for key in master_dic:
        all_team_list.append((master_dic[key]["team_name"], master_dic[key]["BI_list"]))

    all_team_list.sort(key=lambda team: sum(team[1]), reverse=True)

    all_BI_matrix = []
    for i in range(num_weeks):
        for team in all_team_list:
            new_BI = [team[0], "Week " + str(i + 1), team[1][i]]
            all_BI_matrix.append(new_BI)

    df_columns = ["Team", "Week", "BI"]

    df = pd.DataFrame(all_BI_matrix, columns=df_columns)

    fig = px.bar(df, x="Team", y="BI", color="Week", title="Bonage Index")
    figHTML = fig.to_html(full_html=False)
    return figHTML

def get_consistency_graph(master_dic):
    df = pd.DataFrame()

    df["Team"] = [master_dic[team]["team_name"] for team in master_dic]
    df["Standard Deviation"] = [statistics.stdev(master_dic[team]["score_list"]) for team in master_dic]
    df["Average Points Per Week"] = [sum(master_dic[team]["score_list"]) / len(master_dic[team]["score_list"]) for team in master_dic]

    df = df.sort_values(by=['Average Points Per Week'])
    fig = px.scatter(df, title='Consistency vs. Average Performance', y="Standard Deviation", x="Average Points Per Week", color="Team")
    fig.update_traces(textposition='bottom center')
    fig.update_traces(marker_size=10)
    figHTML = fig.to_html(full_html=False)
    return figHTML