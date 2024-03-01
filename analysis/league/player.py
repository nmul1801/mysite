class Player:
    def __init__(self, round_pick, round_num, name, position, pos_rank, on_team_id, stats, id):
        self.round_pick = round_pick
        self.round_num = round_num
        self.name = name
        self.pos_rank = pos_rank
        self.on_team_id = on_team_id
        self.position = position
        self.stats = stats
        self.id = id
        self.first_init = name[0]
        self.last_name = name.split(' ', 1)[1]