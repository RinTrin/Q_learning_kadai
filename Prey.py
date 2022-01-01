import random
import utils

class Prey():
    def __init__(self, edge_len):
        self.edge_len = edge_len

        self.position = [0,0]
        self.way_list = ['up','down','left','right']

        self.hunter_1 = None
        self.hunter_2 = None

    def initialize_position(self):
        x = random.randint(0,self.edge_len-1)
        y = random.randint(0,self.edge_len-1)
        self.position = [x, y]

    def move(self):
        # choose way to move
        move_way_list = utils.check_edge(self.way_list.copy(), self.position, self.edge_len)
        move_way = random.choice(move_way_list)

        # update self.position
        next_pos = utils.update_position(self.position, move_way)
        if self.check_another_agent(next_pos):
            pass
        else:
            self.position = next_pos

    def check_another_agent(self, next_pos):
        if next_pos==self.hunter_1.position or next_pos==self.hunter_2.position:
            return True
        else:
            return False