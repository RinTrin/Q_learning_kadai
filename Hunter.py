import random
import utils
import numpy as np

class Hunter():
    def __init__(self, alpha, gannma, epsilon, edge_len, prey, logger):
        self.alpha = alpha
        self.gannma = gannma
        self.edge_len = edge_len

        self.another_hunter = None
        self.prey = prey
        self.logger = logger

        self.way_list = ['up','down','left','right']
        self.way2num_dic = {way:i for i, way in enumerate(self.way_list)}

        self.position = [0,0]

        self.Q = np.zeros((4, 26, 26))
        self.epsilon = epsilon
        self.r = -1
        self.r_catched = 100

    def initialize_position(self):
        x = random.randint(0,self.edge_len-1)
        y = random.randint(0,self.edge_len-1)

        self.position = [x, y]

        self.array_25 = np.zeros((self.edge_len, self.edge_len))

    def check_25(self):
        x = self.position[0]
        y = self.position[1]
        margin_dic= self.check_margin(x, y)
        agp_array = np.zeros((self.edge_len, self.edge_len))
        agp_array[self.another_hunter.position[0]][self.another_hunter.position[1]] = 1
        agp_array[self.prey.position[0]][self.prey.position[1]] = 2
        # print('AGP', agp_array)
        self.array_25 = self.make_array_25(agp_array, x, y, margin_dic)
        # print(f'x : {x}, y : {y}')
        # print(margin_dic)
        # print(self.array_25)
        # self.array_25 's 1 -> another_hunter's pos
        # self.array_25 's 2 -> prey's pos
    
    def check_25_last(self):
        x = self.another_hunter.position[0]
        y = self.another_hunter.position[1]
        margin_dic= self.check_margin(x, y)
        agp_array = np.zeros((self.edge_len, self.edge_len))
        agp_array[self.position[0]][self.position[1]] = 1
        agp_array[self.prey.position[0]][self.prey.position[1]] = 2
        # print('AGP', agp_array)
        self.array_25 = self.make_array_25(agp_array, x, y, margin_dic)
    
    def check_another_agent(self, next_pos):
        if next_pos==self.prey.position or next_pos==self.another_hunter.position:
            return True
        else:
            return False

    
    def check_margin(self, x, y):
        margin_dic = {way:2 for way in self.way_list}
        left_mar = y
        right_mar = (self.edge_len-1)-y
        up_mar = x
        down_mar = (self.edge_len-1)-x
        mar_list = [up_mar, down_mar, left_mar, right_mar]
        for way_mar, (key, value) in zip(mar_list, margin_dic.items()):
            if 0 <= way_mar < value:
                margin_dic[key] = way_mar
        return margin_dic
    
    def choose_max_way(self, another_hunter_index, prey_index):
        is_epsilon = np.random.choice([True, False], p=[self.epsilon, float(1-self.epsilon)])
        way_able_list = utils.check_edge(self.way_list.copy(), self.position, self.edge_len)
        if is_epsilon:
            # choose random
            max_way = np.random.choice(way_able_list)
        else:
            # choose max_Q
            max_way = None
            max_way_Q = float('inf') * (-1)
            for way in way_able_list:
                way_num = self.way2num_dic[way]
                way_Q = self.Q[way_num][another_hunter_index][prey_index]
                if way_Q > max_way_Q:
                    max_way = way
                    max_way_Q = way_Q
        
        return max_way

    
    def make_array_25(self, array, x, y, margin_dic):
        # print(x-margin_dic['up'],x+margin_dic['down']+1)
        # print(y-margin_dic['left'],y+margin_dic['right']+1)
        return array[x-margin_dic['up']:x+margin_dic['down']+1, y-margin_dic['left']:y+margin_dic['right']+1]
    
    def make_index(self, is_another=True):
        if is_another:key=1
        else:key=2

        if len(self.array_25)==0:
            return 25

        index = list(np.where(self.array_25.reshape(1, -1)[0]==key)[0])
        if index==[]:
            index = 25
        else:
            index = index[0]
        return index
        
    def move_one_step(self, way):
        x = self.position[0]
        y = self.position[1]
        if way=='up':x-=1
        elif way=='down':x+=1
        elif way=='left':y-=1
        elif way=='right':y+=1
        else:raise ValueError

        return [x, y]

    def update_Q(self):
        another_hunter_index = self.make_index(is_another=True)
        prey_index           = self.make_index(is_another=False)
        
        max_way = self.choose_max_way(another_hunter_index, prey_index)
        max_way_num = self.way2num_dic[max_way]

        # check so that another agent is not positioning to moving place
        next_pos = self.move_one_step(max_way)
        if self.check_another_agent(next_pos):
            pass
        else:
            # update self.position
            self.position = utils.update_position(self.position, max_way)
        
        self.check_25()

        next_another_hunter_index = self.make_index(is_another=True)
        next_prey_index           = self.make_index(is_another=False)
        
        max_Q = self.Q[max_way_num][next_another_hunter_index][next_prey_index]
        now_Q = self.Q[max_way_num][another_hunter_index][prey_index]
        self.logger.info(f'max_Q : {max_Q}')
        self.logger.info(f'now_Q : {now_Q}')
        self.logger.info(f'max_way_num : {max_way_num}, {max_way}')
        self.logger.info(f'another_hunter_index, prey_index : {another_hunter_index}, {prey_index}')
        self.logger.info(f'next_another_hunter_index, next_prey_index : {next_another_hunter_index}, {next_prey_index}')
        if utils.catched(self.position, self.another_hunter.position, prey_position=self.prey.position):
            self.Q[max_way_num][another_hunter_index][prey_index] = (1-self.alpha)*now_Q + self.alpha*(self.r_catched + self.gannma*max_Q)
            self.check_25_last()
            hunter_index = self.make_index(is_another=True)
            prey_index   = self.make_index(is_another=False)
            now_Q = self.Q[max_way_num][hunter_index][prey_index]
            self.another_hunter.Q[max_way_num][hunter_index][prey_index] = (1-self.alpha)*now_Q + self.alpha*(self.r_catched + self.gannma*max_Q)
            return True
        else:
            self.Q[max_way_num][another_hunter_index][prey_index] = (1-self.alpha)*now_Q + self.alpha*(self.r + self.gannma*max_Q)
            return False