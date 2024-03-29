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

        if self.pos_rank == 0:
            self.pos_rank = 999
        self.pos_rank_written = self.set_num(pos_rank)
        self.positional_ = self.set_num(pos_rank)

    def set_num(self, num):
        if num % 10 == 1:
            return str(num) + "st"
        elif num % 10 == 2:
            return str(num) + "nd"
        elif num % 10 == 3:
            return str(num) + "rd"
        else:
            return str(num) + "th"
        
    def set_position_pick(self):
        self.position_pick_written = self.set_num(self.position_pick)
    
    
    