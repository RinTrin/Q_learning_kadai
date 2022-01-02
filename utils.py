import numpy as np
import cv2
import matplotlib.pyplot as plt

import os
import time
import logging
from logging import getLogger

def catched(*pos_all, prey_position=[0, 0]):
    hunter_pos1, hunter_pos2 = pos_all
    h1_x, h1_y = hunter_pos1
    h2_x, h2_y = hunter_pos2
    p_x, p_y   = prey_position

    hunter_near_num = 0
    for h_x, h_y in zip([h1_x,h2_x],[h1_y,h2_y]):
        for px_near, py_near in zip([p_x-1,p_x+1,p_x,p_x],[p_y,p_y,p_y-1,p_y+1]): # up,down,left,right
            if px_near==h_x and py_near==h_y:
                hunter_near_num+=1
                break
            else:
                continue
        if hunter_near_num>=2:
            # print('-----CATCHED-----')
            return True
    # if hunter_near_num>=1:
    #     print(f'hunter_near_num : {hunter_near_num}')
    # print('-----MISSED-----')   # it was ignoreing
    return False

def check_edge(move_way_list, position, edge_len):
    if position[0]==0:
        move_way_list.remove('up')
    elif position[0]==edge_len-1:
        move_way_list.remove('down')
    if position[1]==0:
        move_way_list.remove('left')
    elif position[1]==edge_len-1:
        move_way_list.remove('right')

    return move_way_list

def counter(steps, param=10000):
    if steps % param==0:
        print(f'STEPS  :  {steps}')

def make_logger(prj_name):
    timestr = time.strftime('%Y.%m.%d-%H%M%S')
    LOG_PATH = os.path.join(f'./log/{prj_name}_{timestr}.log')
    logger = getLogger("")

    with open(LOG_PATH, 'w', encoding='UTF-8') as log:
        log.write('')
    logging.basicConfig(level=logging.INFO, filename=LOG_PATH)
    logger = logging.getLogger(__name__)

    return logger

def make_plot(x_list, y_list):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x_list, y_list, color='green', label='Q_learning')
    # ax.scatter(frame_num, y_dic[clr][-1], c=self.plot_color_dic[clr])
    ax.legend(loc=0)
    buf, size = fig.canvas.print_to_buffer()
    # print('size is : ',size)
    img_arr = np.frombuffer(buf, dtype=np.uint8).reshape(size[1], size[0], -1)
    table = cv2.cvtColor(img_arr, cv2.COLOR_RGBA2BGR)
    plt.close()
    return table

def print_debug(hunter_1, hunter_2, prey, edge_len, logger, is_debug=False, is_Q=False):
    # params for printing
    print_str = True

    if not is_debug:
        pass
    else:
        if print_str:
            logger.info(f'HUNTER_1 POSITION  :  {hunter_1.position}')
            logger.info(f'HUNTER_2 POSITION  :  {hunter_2.position}')
            logger.info(f'PREY     POSITION  :  {prey.position}')
        else:
            white = np.zeros((edge_len, edge_len))
            white[hunter_1.position[0]][hunter_1.position[1]] = 1
            white[hunter_2.position[0]][hunter_2.position[1]] = 2
            white[prey.position[0]][prey.position[1]] = 3
            print(white)
        
    if is_Q:
        # logger.info(hunter_1.Q)
        for q in hunter_1.Q:
            logger.info(np.sum(q))

def set_another_agent(hunter_1, hunter_2, prey):
    hunter_1.another_hunter = hunter_2
    hunter_2.another_hunter = hunter_1
    prey.hunter_1 = hunter_1
    prey.hunter_2 = hunter_2

def update_position(position, move_way):
    new_x, new_y = position
    if move_way=='up':
        new_x -= 1
    elif move_way=='down':
        new_x += 1
    elif move_way=='left':
        new_y -= 1
    elif move_way=='right':
        new_y += 1
    else:
        print('\nWRONG WAY ARE CHOSEN\n')
        raise ValueError

    new_position = [new_x, new_y]
    return new_position

if __name__=='__main__':
    a = catched([1,0],[0,2], prey_position=[0, 0])
    print(a)