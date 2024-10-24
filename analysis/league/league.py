from espn_api.football import League as ESPN_League
from analysis.league.team import Team
from analysis.league.player import Player
import requests
import pandas as pd
import math
import plotly.express as px
from scipy.stats import norm
import statistics
import requests
import json
from django.conf import settings
import os
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import simps

class League:

    # Constructor for league object - takes in platform, as well as any identifying league parameters
    def __init__(self, platform, league_id, s2=None, swid=None):
        print('initializing league')
        self.platform = platform
        self.start_week = 0
        self.num_weeks = self.get_cur_finished_nfl_week()
        # cases for constructing league
        if platform == 'espn':
            # catch where league doesn't exist
            try: 
                league_ob = ESPN_League(league_id=league_id, year=2024, espn_s2=s2, swid=swid)
            except Exception as e:
                # error case 
                return None
            
            self._construct_league_espn(league_ob)
        
        elif platform == 'sleeper':
            # try to get response, error if none
            r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id) + "/rosters")
            if r.status_code != 200:
                # return error if sleeper league isn't found
                return None
                # return render(request, 'index.html', context={'error_code': 1})
            
            self._construct_league_sleeper(league_id)

        self._construct_league_general()

        self.primary_color = '#574D68'
        self.secondary_color = '#DDC9B4'

    # League construction based on platform
            
    def _construct_league_espn(self, league):
        self.random_team_lineup = []
        self.num_teams = len(league.teams)
        self.teams = {}


        for team in league.teams:
            self.teams[team.team_id] = Team(team.team_id)
            self.teams[team.team_id].set_team_name(team.team_name)
            self.teams[team.team_id].set_score_list(team.scores[:self.num_weeks])
            self.teams[team.team_id].set_win_list(list(map(lambda x: 1 if x == 'W' else 0, team.outcomes)))

        for i in range(1, self.num_weeks + 1):
            for box_score in league.box_scores(week=i):
                if box_score.home_team.team_id == 8:
                    self.random_team_lineup.append(box_score.home_lineup)
                if box_score.away_team.team_id == 8:
                    self.random_team_lineup.append(box_score.away_lineup)
                    
                home_id, away_id = box_score.home_team.team_id, box_score.away_team.team_id
                

                self.teams[home_id].append_opp_id(away_id)
                self.teams[away_id].append_opp_id(home_id)
        
        self._construct_draft_espn(league)

    def _construct_draft_espn(self, league):
        # all draft picks
        print('constructing draft list')
        self.draft_rounds = {}
        player_id_to_team_dict = {}
        player_id_list = list()
        # crete dictionary to recall where players went in the draft
        for pick in league.draft:
            player_pick_info = (pick.round_num, pick.round_pick, pick.team.team_id)
            player_id_to_team_dict[pick.playerId] = player_pick_info
            # use player_id to get all players in one call
            player_id_list.append(pick.playerId)          

        # get all draft picks
        player_class_list = league.player_info(playerId = player_id_list)

        for p_class in player_class_list:
            round_num, round_pick, on_roster_id = player_id_to_team_dict[p_class.playerId]
            player_c = Player(round_pick, round_num, p_class.name, p_class.position, p_class.posRank, on_roster_id, p_class.stats, p_class.playerId)
            if player_c.position == 'D/ST' or player_c.position == 'K':
                continue
            self.teams[on_roster_id].append_draft_pick(round_num, round_pick, player_c)
            
            if round_num in self.draft_rounds:
                self.draft_rounds[round_num][round_pick] = player_c
            else:
                self.draft_rounds[round_num] = {round_pick : player_c}
                
        print('done with draft')

    def _construct_league_sleeper(self, league_id):
        # load resources
        r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id))
        league_ob = json.loads(r.text)

        r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id) + "/rosters")
        rosters_ob = json.loads(r.text)

        r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id) + "/users")
        users_ob = json.loads(r.text)

        self.draft_id = league_ob['draft_id']

        # get display names
        user_id_to_disp_name = {o['user_id'] : o['display_name'] for o in users_ob}
        
        self.teams = dict({ros['roster_id']: Team(ros['roster_id']) for ros in rosters_ob})
        self.num_teams = len(self.teams)

        # used for translating wins
        mapping_wins = {"W": 1, "T": 0.5, "L": 0}    

        # first run through of league - easy info
        for ros in rosters_ob:
            # instance of Team class
            cur_team = self.teams[ros['roster_id']]

            # set team name, wins
            cur_team.set_team_name(user_id_to_disp_name[ros['owner_id']])
            
            win_list_mapped = [mapping_wins[g] for g in ros['metadata']['record']]
            
            # remove average matches if league has them (every other match from the win list)
            if league_ob['settings']['league_average_match'] == 1:
                win_list_mapped = win_list_mapped[::2]
            
            cur_team.set_win_list(win_list_mapped)

        # iterate through weeks
        for i in range(1, self.num_weeks + 1):
            r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id) + "/matchups/" + str(i))
            matchup_ob = json.loads(r.text)
            matchcup_dic = {}

            for match_ob in matchup_ob:
                m_id, r_id = match_ob['matchup_id'], match_ob['roster_id']
                # score list
                self.teams[r_id].append_score_list(match_ob['points'])
                # opponent id list
                if m_id in matchcup_dic:
                    self.teams[r_id].append_opp_id(matchcup_dic[m_id])
                    self.teams[matchcup_dic[m_id]].append_opp_id(r_id)
                else:
                    matchcup_dic[m_id] = r_id

        self._construct_draft_sleeper(league_id)

    def _construct_draft_sleeper(self, league_id):
        r = requests.get(url="https://api.sleeper.app/v1/draft/" + str(self.draft_id) + "/picks")

        draft_ob = json.loads(r.text)

        r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id))
        league_ob = json.loads(r.text)
        league_positions = league_ob['roster_positions']
        
        path = os.path.join(settings.BASE_DIR, 'analysis/static/data/allPlayerData.json')

        with open(path,"r") as file:
            player_data = json.load(file)
        # used to get the player position ranks
        league = ESPN_League(league_id=1927423163, year=2024, espn_s2='AECM85hbXZD%2FFG9s2ALIuE4XrHUPYodyji1oDVpO17ISfafgY9b9kxJ4QZaG1FiR1nVU0UW%2FtIQoPvtOfxxlA2y9xKn4dFzG1FO%2BNdP6ZsZZNly5BCtfCznME5sc8OJhBcY7nEjYRQ6b6tAtQvXYyvV65Ya6Hk4klxd0iIBzk6S82ZZiob5i8%2BThUSpeh0sUypUA%2FdpC06ZhaEVy9B0qVL%2B3tL8T3pK44imaNmSCGrLEmtTb5xmhmKIQYPPmE99IEvNy9ltr9DfPmJucfiPMVAfBcWaZUpEAE160r4SsIszqsw%3D%3D', swid='F71F32C4-9869-4DFB-A620-ADD15AA67520')
        player_id_to_team_dict, self.draft_rounds = {}, {}
        player_name_list = list()
        # get all players with an espn id
        for pick in draft_ob:
            # get the player
            player_id = pick['player_id']
            data = player_data[player_id]

            # filter out silly picks and defensive picks
            if data['position'] not in league_positions or data['position'] == 'DEF' or data['position'] == 'K':
                continue
            
            # take count of their name if we have to, but try to get espn id 
            if data['espn_id'] == None:
                player_name_list.append((data['full_name'], pick["round"], pick["draft_slot"], pick["roster_id"]))
            else:
                player_id_to_team_dict[data['espn_id']] = pick["round"], pick["draft_slot"], pick["roster_id"]
        
        if len(player_id_to_team_dict) != 0:
            player_class_list = league.player_info(playerId = list(player_id_to_team_dict.keys()))

            for p_class in player_class_list:
                round_num, round_pick, on_roster_id = player_id_to_team_dict[p_class.playerId]
                self._add_draft_pick(round_num, round_pick, on_roster_id, p_class)
            
        for full_name, round_num, pick_num, on_team_id in player_name_list:
            p_class = league.player_info(name=full_name)
            # try with jr
            if p_class == None:
                p_class = league.player_info(name=full_name + " Jr.")

            # try with III
            if p_class == None:
                p_class = league.player_info(name=full_name + " III")

            if p_class == None:
                print('FAILED')
                continue
            # now with name, assemble the player
            self._add_draft_pick(round_num, pick_num, on_team_id, p_class)

    def _add_draft_pick(self, round_num, pick_num, on_team_id, p_class):
        player = Player(pick_num, round_num, p_class.name, p_class.position, p_class.posRank, on_team_id, dict(p_class.stats), p_class.playerId)
        cur_team = self.teams[on_team_id]
        cur_team.append_draft_pick(round_num, pick_num, player)

        if round_num in self.draft_rounds:
            self.draft_rounds[round_num][pick_num] = player
        else:
            self.draft_rounds[round_num] = {pick_num : player}

    # after getting all info from team dictionary, extrapolate other analysis
    def _construct_league_general(self):
        # rank list
        for i in range(self.num_weeks):
            weekly_id_scores_dic = {k : {'score': self.teams[k].get_score_at(i)} for k in self.teams}

            weekly_id_scores_dic = dict(sorted(weekly_id_scores_dic.items(), key=lambda x: x[1]['score'], reverse=True))
            scores_isolated = [weekly_id_scores_dic[k]['score'] for k in weekly_id_scores_dic]
            rank_list = self._create_rank_list(scores_isolated)
            for i, ros_id in enumerate(weekly_id_scores_dic):
                self.teams[ros_id].append_rank(rank_list[i])

        # opponent_rank_list
        for r_id in self.teams:
            opp_rank_list = list()
            for i, opp_id in enumerate(self.teams[r_id].get_opp_id_list()):
                opp_rank_list.append(self.teams[opp_id].get_rank_at(i))
            self.teams[r_id].set_opp_rank_list(opp_rank_list)

        # BI and ew
        for t in self.teams.values():
            bi_list = [self.num_teams - r + 1 for r in t.get_opp_rank_list()]
            t.set_bi_list(bi_list)

            ew_list  = [round((self.num_teams - r) / (self.num_teams - 1), 2) for r in t.get_rank_list() ]
            t.set_ew_list(ew_list)

        # sort drafts
        # general league 
        for r, draft_round_dict in self.draft_rounds.items():
            self.draft_rounds[r] = dict(sorted(draft_round_dict.items(), key=lambda x: x[0]))
            
        self.draft_rounds = dict(sorted(self.draft_rounds.items(), key=lambda x: x[0]))

        # teams specific
        for t in self.teams.values():
            # get team draft picks
            draft_dict = t.get_draft_picks()
            for r_num, round_picks in draft_dict.items():
                draft_dict[r_num] = dict(sorted(round_picks.items(), key=lambda x: x[0]))
            
            # sort each team dict by round
            draft_dict = dict(sorted(draft_dict.items(), key=lambda x: x[0]))
            t.set_draft_picks(draft_dict)

        # set percent injured
        for round_num, picks_dict in self.draft_rounds.items():
            for p_num, p in picks_dict.items():
                num_week_injured = 0
                for week_num in range(1, self.num_weeks + 1):
                    if week_num not in p.stats:
                        num_week_injured += 1
                    elif len(p.stats[week_num]['breakdown']) == 0:
                        num_week_injured += 1

                p.percent_injured = num_week_injured / self.num_weeks

    def _get_num_weeks_sleeper(self, league_id):
        r = requests.get(url="https://api.sleeper.app/v1/league/" + str(league_id))
        league_ob = json.loads(r.text)
        p_start = league_ob['settings']['playoff_week_start']
        return p_start - 1
    
    def _create_rank_list(self, num_list):
        ranked_list = [1]
        for i, cur_score in enumerate(num_list):
            if i == 0: continue
            if cur_score == num_list[i - 1]:
                ranked_list.append(ranked_list[-1])
            else:
                ranked_list.append(i + 1)
        return ranked_list 
    
    def get_cur_finished_nfl_week(self):
        res_nfl = requests.get(url="https://api.sleeper.app/v1/state/nfl")
        nfl_ob = json.loads(res_nfl.text)    
        return nfl_ob['week'] - 1

    def get_average_pos_rank_graph(self, half=1):
        all_avgs = []
        # teams
        for t in self.teams.values():
            # draft rounds
            avg_pos_rank_by_round_list = list()
            for round_picks in t.get_draft_picks().values():
                pos_ranks = [pick.pos_rank for pick in round_picks.values()]
                avg_pos_rank = sum(pos_ranks) / len(pos_ranks) if len(pos_ranks) != 0 else 0
                avg_pos_rank_by_round_list.append(avg_pos_rank)
                
            if half == 1:
                half_list = avg_pos_rank_by_round_list[:len(avg_pos_rank_by_round_list)//2]
            else:
                half_list = avg_pos_rank_by_round_list[len(avg_pos_rank_by_round_list)//2:]

            avg_half_list = (sum(half_list) / len(half_list)) if len(half_list) != 0 else 0

            all_avgs.append([t.get_name(), avg_half_list])

        df_columns = ["Team", "Average Positional Rank"]

        df = pd.DataFrame(all_avgs, columns=df_columns)
        df = df.sort_values(by='Average Positional Rank')

        fig = px.bar(df, x="Team", y="Average Positional Rank", color_discrete_sequence=[self.primary_color])
        fig.update_layout(
            xaxis_title=''
        )
        figHTML = self._create_fig_layout(fig, include_legend=False)
        return figHTML
    
    def get_sleepers(self):
        position_picks_dic = {}
        for draft_round in self.draft_rounds.values():
            for p in draft_round.values():
                if p.position in position_picks_dic:
                    position_picks_dic[p.position].append(p)
                    p.position_pick = len(position_picks_dic[p.position])
                else:
                    p.position_pick = 1
                    position_picks_dic[p.position] = [p]
                p.set_position_pick()
                p.sleeper_score = p.position_pick - p.pos_rank
        sleeper_dict = {pos : max(position_picks_dic[pos], key=lambda x: x.sleeper_score) for pos in position_picks_dic}
        return sleeper_dict

    def get_draft_injury_table(self):
        draft_table_dict = {i : {j : list() for j in self.teams.keys()} for i in range(1, len(self.draft_rounds) + 1)}

        for round_num, picks in self.draft_rounds.items():
            for pick_num, p in picks.items():
                draft_table_dict[round_num][p.on_team_id].append({'name': p.name, 'percent_injured': p.percent_injured})
    
    def _create_rank_list(self, num_list):
        ranked_list = [1]
        for i, cur_score in enumerate(num_list):
            if i == 0: continue
            if cur_score == num_list[i - 1]:
                ranked_list.append(ranked_list[-1])
            else:
                ranked_list.append(i + 1)
        return ranked_list

    def get_expected_wins_graph(self):
        all_team_list = list()
        for t in self.teams.values():
            (name, ew_list, win_list) = t.get_name(), t.get_ew_list(), t.get_wins()
            all_team_list.append((name, ew_list, win_list))

        all_team_list.sort(key=lambda team: sum(team[1]), reverse=True)

        all_wins_matrix = []
        for i in range(self.num_weeks):
            for team in all_team_list:
                new_ew = [team[0], "Week " + str(i + 1), team[1][i]]
                all_wins_matrix.append(new_ew)
                
        df_columns = ["Team", "Week", "Expected Wins"]

        color_map = {"Week " + str(i + 1): self.primary_color if i % 2 == 0 else self.secondary_color for i in range(self.num_weeks)}

        df = pd.DataFrame(all_wins_matrix, columns=df_columns)

        fig = px.bar(df, x="Team", y="Expected Wins", color="Week", color_discrete_map=color_map)
        
        figHTML = self._create_fig_layout(fig, True)
        return figHTML

    def get_ew_difference_graph(self):
        
        ew_diff_dict = {t.id : sum(t.get_wins()) - sum(t.get_ew_list()) for t in self.teams.values()}
        ew_diff_dict = dict(sorted(ew_diff_dict.items(), key=lambda x: x[1], reverse=True))


        # dictionary for team display

        lucky_team = self.teams[list(ew_diff_dict.items())[0][0]]
        unlucky_team = self.teams[list(ew_diff_dict.items())[-1][0]]

        self.lucky_team = lucky_team
        self.lucky_team_ew_diff = round(sum(lucky_team.get_wins()) - sum(lucky_team.get_ew_list()), 2)

        ew_team_dic = {'lucky_name' : lucky_team.get_name(), 
                        'l_total_wins' : round(sum(lucky_team.get_wins()), 2), 
                        'l_total_ex_wins' : round(sum(lucky_team.get_ew_list()), 2),
                        'l_ew_diff' : round(sum(lucky_team.get_wins()) - sum(lucky_team.get_ew_list()), 2),
                        'unlucky_name' : unlucky_team.get_name(), 
                        'u_total_wins' : round(sum(unlucky_team.get_wins()), 2), 
                        'u_total_ex_wins' : round(sum(unlucky_team.get_ew_list()), 2),
                        'u_ew_diff' : round(sum(unlucky_team.get_ew_list()) - sum(unlucky_team.get_wins()), 2)
                        }

        all_diff_matrix = []
        for ew_entry in ew_diff_dict.items():
            all_diff_matrix.append([self.teams[ew_entry[0]].get_name(), ew_entry[1]])

        df_columns = ["Team", "EW Difference"]

        df = pd.DataFrame(all_diff_matrix, columns=df_columns)

        fig = px.bar(df, x="Team", y="EW Difference", color_discrete_sequence=[self.primary_color])
        figHTML = self._create_fig_layout(fig, False)
        
        return ew_team_dic, figHTML
    
    def get_luck_graph(self):
        ew_diff_dict = {t.get_name() : sum(t.get_wins()) - sum(t.get_ew_list()) for t in self.teams.values()}
        ew_diff_dict = dict(sorted(ew_diff_dict.items(), key=lambda x: x[1]))

        n = self.num_weeks
        p = 0.5
        variance = n * p * (1 - p)
        luck_P_list = list()

    
        for ew in ew_diff_dict.values():
            z_score = ew / math.sqrt(variance) if variance != 0 else 0
            p = norm.cdf(z_score)
            luck_P_list.append(round((p * 100), 2))

        luck_dic = {'l_prob' : luck_P_list[-1], 'u_prob': luck_P_list[0], 'perc_lucky' : round(100 - luck_P_list[0], 2)}

        luck_matrix = []
        for i, entry in enumerate(ew_diff_dict.items()):
            new_luck = [entry[0], luck_P_list[i]]
            luck_matrix.append(new_luck)

        df_columns = ["Team", "Likelihood of Performing Worse"]

        df = pd.DataFrame(luck_matrix, columns=df_columns)

        fig = px.bar(df, 
            x="Team", 
            y="Likelihood of Performing Worse",
            color_discrete_sequence=[self.primary_color]
            )
        
        

        fig.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="Line of Luck", annotation_position="top left")

        figHTML = self._create_fig_layout(fig, True)
        
        return luck_dic, figHTML

    def get_bonage_graph(self):
        all_team_list = list()
        for t in self.teams.values():
            all_team_list.append((t.get_name(), t.get_bi_list()))

        all_team_list.sort(key=lambda team: sum(team[1]), reverse=True)

        all_BI_matrix = []
    
        for i in range(self.num_weeks):
            for team in all_team_list:
                new_BI = [team[0], "Week " + str(i + 1), team[1][i]]
                all_BI_matrix.append(new_BI)

        df_columns = ["Team", "Week", "BI"]

        df = pd.DataFrame(all_BI_matrix, columns=df_columns)

        color_map = {"Week " + str(i + 1): self.primary_color if i % 2 == 0 else self.secondary_color for i in range(self.num_weeks)}

        fig = px.bar(df, x="Team", y="BI", color="Week", color_discrete_map=color_map)

        figHTML = self._create_fig_layout(fig, True)

        return figHTML
    
    def get_consistency_graph(self):
        df = pd.DataFrame()

        df["Team"] = [t.get_name() for t in self.teams.values()]
        df["Consistency Score"] = [ 100 - ((statistics.stdev(t.get_score_list()) / (sum(t.get_score_list()) / self.num_weeks)) * 100) for t in self.teams.values()]
        df["Average Points Per Week"] = [sum(t.get_score_list()) / self.num_weeks for t in self.teams.values()]

        df = df.sort_values(by=['Average Points Per Week'])
        fig = px.scatter(df, y="Consistency Score", x="Average Points Per Week", color="Team")
        fig.update_traces(textposition='bottom center')
        fig.update_traces(marker_size=10)
        figHTML = self._create_fig_layout(fig, True)
        return figHTML
    
    def get_pos_rank_through_draft_graph(self):
        pos_rank_avg = list()
        for d_round in self.draft_rounds.values():
            pos_rank_list = [p.pos_rank for p in  d_round.values()]
            pos_rank_avg.append(sum(pos_rank_list) / len(pos_rank_list))
        df = pd.DataFrame({
            'Draft Round' : range(1, len(pos_rank_avg) + 1),
            'Average Positional Rank' : pos_rank_avg
        }
        )
        fig = px.line(df, x="Draft Round", y="Average Positional Rank", color_discrete_sequence=[self.primary_color])
        figHTML = self._create_fig_layout(fig, False)
        return figHTML
    
    def get_draft_injury_table(self):
        color_list = ['black', 'red', '#f13600', '#e36500', '#d58e00', '#c7b000', '#a4b800', '#72aa00', '#459c00', '#208e00', 'green']

        draft_table_dict = {i : {j : list() for j in self.teams.keys()} for i in range(1, len(self.draft_rounds) + 1)}

        for round_num, picks in self.draft_rounds.items():
            for pick_num, p in picks.items():
                ind = 9 - int(p.percent_injured * 10 * 2)
                ind = 0 if ind < 0 else ind
                c = color_list[ind]

                draft_table_dict[round_num][p.on_team_id].append({'name': p.name, 'percent_inj': round(p.percent_injured * 100, 2), 'id': p.id, 'bg_color': c})
        
        for round_num, picks in draft_table_dict.items():
            max_length = max([len(l) for l in list(picks.values())])
            for team_id in picks:
                picks[team_id] += [None] * (max_length - len(picks[team_id]))

        draft_adjusted_dic = {r_num : [] for r_num in draft_table_dict}
        for round_num, picks in draft_table_dict.items():
            picks_list = list(picks.values())
            for i in range(len(picks_list[0])):
                pick_series = []
                for team_picks in picks_list:
                    pick_series.append(team_picks[i])
                draft_adjusted_dic[round_num].append(pick_series)
        
        # print(draft_adjusted_dic)
        return draft_adjusted_dic

    def get_probdcurve(self):
        # Function to calculate the probability density function (PDF) of the normal distribution
        def normal_pdf(x, mean, standard_deviation):
            return 1 / (standard_deviation * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mean) / standard_deviation)**2)

        num_games = self.num_weeks
        p = 0.5
        var = num_games * p * (1 - p)

        mean = 0  # Mean of the distribution
        standard_deviation = np.sqrt(var)  # Standard deviation of the distribution
        x_values = np.linspace(-5, 5, 100)  # Adjust range as needed
        y_values = normal_pdf(x_values, mean, standard_deviation)

        fig = px.line(x=x_values, y=y_values, title='Normal Distribution Curve')
        
        x_shade = self.lucky_team_ew_diff  # Adjust as needed

        # Generate the x and y values for shading
        x_shade_values = np.linspace(-5, x_shade, 1000)
        y_shade_values = normal_pdf(x_shade_values, mean, standard_deviation)

        area_under_curve = simps(y_shade_values, x_shade_values)

        fig.add_trace(
            go.Scatter(
                x=np.concatenate([x_shade_values, x_shade_values[::-1]]),
                y=np.concatenate([y_shade_values, [0]*len(y_shade_values)]),
                fill='toself',
                fillcolor='rgba(0,100,80,0.2)',  # Adjust transparency as needed
                line=dict(color='rgba(255,255,255,0)'),
                name=f'Area under the curve up to x={x_shade}'
            )
        )

        fig.add_trace(go.Scatter(x=[x_shade], y=[normal_pdf(x_shade, mean, standard_deviation)], mode='markers', name='Point'))
        fig.add_annotation(x=x_shade, y=normal_pdf(x_shade, mean, standard_deviation), text=f'Luck metric for {self.lucky_team.get_name()}<br>Wins - Expected wins = {self.lucky_team_ew_diff}<br>Area under curve = {area_under_curve:.2f}', showarrow=True, arrowhead=1)
        fig.update_layout(title='Normal Distribution Curve with Labeled Point', xaxis_title='x', yaxis_title='Probability Density')

        # Show the plot
        fig.update_layout(showlegend=False)

        return self._create_fig_layout(fig, False)


    def _create_fig_layout(self, fig, include_legend):

        fig.update_layout(
            showlegend=include_legend,
            margin=dict(l=0, r=0, t=0, b=0),  # Set margins to zero to remove extra space
            xaxis_tickangle=-60,
            # plot_bgcolor='white',  # Set background color
            # paper_bgcolor='white',
            font=dict(color='black'),  # Set text color
            xaxis=dict(tickfont=dict(color='black')),  # Set x-axis tick labels color
            yaxis=dict(tickfont=dict(color='black'))
        )


        if include_legend:
            fig.update_layout(
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )

        fig_html = fig.to_html(full_html=False, config={'dragmode': 'orbit', 'scrollZoom': False, 'displayModeBar': False})

        return fig_html
