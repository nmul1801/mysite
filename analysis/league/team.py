class Team:
    
    def __init__(self, id):
        self.id = id
        self.opp_rank_list = list()
        self.opp_id_list = list()
        self.rank_list = list()
        self.ew_list = list()
        self.bi_list = list()
        self.score_list = list()
        self.win_list = list()
        # dictionary of round : players
        self.draft_picks = {}
        self.box_lineup = {}
    
    def set_team_name(self, name):
        self.name = name

    def set_win_list(self, win_list):
        self.win_list = win_list

    def set_score_list(self, score_list):
        self.score_list = score_list

    def append_score_list(self, score):
        self.score_list.append(score)
        
    def append_rank(self, rank):
        self.rank_list.append(rank)

    def append_opp_rank(self, opp_rank):
        self.opp_rank_list.append(opp_rank)
    
    def append_opp_id(self, opp_id):
        self.opp_id_list.append(opp_id)

    def append_draft_pick(self, round_num, round_pick, player):
        if round_num in self.draft_picks.keys():
            self.draft_picks[round_num][round_pick] = player
        else:
            self.draft_picks[round_num] = {round_pick : player}

    def set_draft_picks(self, draft_picks):
        self.draft_picks = draft_picks
    
    def get_draft_picks(self):
        return self.draft_picks

    def set_opp_rank_list(self, opp_rank_list):
        self.opp_rank_list = opp_rank_list

    def set_bi_list(self, bi_list):
        self.bi_list = bi_list
    
    def set_ew_list(self, ew_list):
        self.ew_list = ew_list

    def get_ew_list(self):
        return self.ew_list
    
    def get_bi_list(self):
        return self.bi_list

    def get_wins(self):
        return self.win_list

    def get_opp_id_list(self):
        return self.opp_id_list

    def get_team_opp_rank_list(self):
        return self.opp_rank_list

    def get_score_at(self, i):
        return self.score_list[i]

    def get_score_list(self):
        return self.score_list

    def get_rank_at(self, i):
        return self.rank_list[i]
    
    def get_rank_list(self):
        return self.rank_list
    
    def get_opp_rank_list(self):
        return self.opp_rank_list
    
    def get_name(self):
        return self.name