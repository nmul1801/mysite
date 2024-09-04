import pandas as pd
import math
import plotly.express as px
from scipy.stats import norm
import statistics
import requests
import json

# espn league construction
# all we need to return is dict with team name, opp_id_list, win list, scores
def construct_raw_team_dic_espn(league):
    cur_nfl_week = get_cur_finished_nfl_week()
    reg_szn_games = league.settings.reg_season_count
    num_weeks = reg_szn_games

    master_dic = {}
    for team in league.teams:
        master_dic[team.team_id] = {"team_name" : team.team_name, 
                                "opp_id_list": list(),
                                "rank_list": list(),
                                "score_list" : team.scores}
        master_dic[team.team_id]["win_list"] = list(map(lambda x: 1 if x == 'W' else 0, team.outcomes))

    for i in range(1, num_weeks + 1):
        for box_score in league.box_scores(week=i):
            home_id, away_id = box_score.home_team.team_id, box_score.away_team.team_id

            master_dic[home_id]["opp_id_list"].append(away_id)
            master_dic[away_id]["opp_id_list"].append(home_id)

    return master_dic, num_weeks

# sleeper team dictionary construction
# all we need to return is dict with team name, opp_id_list, win list, scores
def construct_raw_team_dic_sleeper(league_id):
    num_weeks = get_num_weeks_sleeper(league_id)

    r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id))
    league_ob = json.loads(r.text)
    
    r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id) + "/rosters")
    rosters_ob = json.loads(r.text)

    r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id) + "/users")
    users_ob = json.loads(r.text)
    user_id_to_disp_name = {o['user_id'] : o['display_name'] for o in users_ob}

    roster_dic = dict({ros['roster_id']: {"opp_rank_list" : list(), 
                                          "rank_list" : list(), 
                                          "ew_list": list(), 
                                          "BI_list": list(), 
                                          "score_list": list(),
                                          "opp_id_list": list(), 
                                          "win_list": list()} for ros in rosters_ob})
    mapping_wins = {"W": 1, "T": 0.5, "L": 0}

    for ros in rosters_ob:
        cur_roster_num = ros['roster_id']
        # team name
        roster_dic[cur_roster_num]['team_name'] = user_id_to_disp_name[ros['owner_id']]
        # win list
        roster_dic[cur_roster_num]['win_list'] = [mapping_wins[g] for g in ros['metadata']['record']]
        # remove every other match from the win list
        if league_ob['settings']['league_average_match'] == 1:
            roster_dic[cur_roster_num]['win_list'] = roster_dic[cur_roster_num]['win_list'][::2]

    # loop thru all weeks
    for i in range(1, num_weeks + 1):
        r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id) + "/matchups/" + str(i))
        matchup_ob = json.loads(r.text)

        matchcup_dic = {}
        # iterate thru all matches for given week
        for match_ob in matchup_ob:
            m_id, r_id = match_ob['matchup_id'], match_ob['roster_id']
            # score list
            roster_dic[match_ob['roster_id']]['score_list'].append(match_ob['points'])
            # opponent id list
            if m_id in matchcup_dic:
                roster_dic[r_id]['opp_id_list'].append(matchcup_dic[m_id])
                roster_dic[matchcup_dic[m_id]]['opp_id_list'].append(r_id)
            else:
                matchcup_dic[m_id] = r_id

    return roster_dic, num_weeks

# after getting all info from team dictionary, extrapolate other analysis
def construct_team_dic(team_dic, num_weeks):
    # rank list
    for i in range(num_weeks):
        weekly_id_scores_dic = {k : {'score': team_dic[k]['score_list'][i]} for k in team_dic}
        weekly_id_scores_dic = dict(sorted(weekly_id_scores_dic.items(), key=lambda x: x[1]['score'], reverse=True))
        scores_isolated = [weekly_id_scores_dic[k]['score'] for k in weekly_id_scores_dic]
        rank_list = create_rank_list(scores_isolated)
        for i, ros_id in enumerate(weekly_id_scores_dic):
            team_dic[ros_id]['rank_list'].append(rank_list[i])

    # opponent_rank_list
    for r_id in team_dic:
        opp_rank_list = list()
        for i, opp_id in enumerate(team_dic[r_id]['opp_id_list']):
            opp_rank_list.append(team_dic[opp_id]['rank_list'][i])
        team_dic[r_id]['opp_rank_list'] = opp_rank_list

    # BI and ew
    for t in team_dic:
        team_dic[t]["BI_list"] = [len(team_dic) - r + 1 for r in team_dic[t]['opp_rank_list']]
        team_dic[t]["ew_list"] = [round((len(team_dic) - r) / (len(team_dic) - 1), 2) for r in team_dic[t]['rank_list']]
    
    return team_dic, num_weeks

def get_num_weeks_sleeper(league_id):
    r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id))
    league_ob = json.loads(r.text)
    p_start = league_ob['settings']['playoff_week_start']
    return p_start - 1

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
        z_score = team[1] / math.sqrt(variance) if variance != 0 else 0
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

    df_columns = ["Team", "Week", "OI"]

    df = pd.DataFrame(all_BI_matrix, columns=df_columns)

    fig = px.bar(df, x="Team", y="OI", color="Week", title="Ownage Index")
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