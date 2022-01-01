import numpy as np
import cv2
import matplotlib.pyplot as plt

def catched(*pos_all, prey_position=[0, 0]):
    hunter_pos1, hunter_pos2 = pos_all
    h1_x, h1_y = hunter_pos1
    h2_x, h2_y = hunter_pos2
    p_x, p_y   = prey_position

    hunter_near_num = 0
    for h_x, h_y in zip([h1_x,h2_x],[h1_y,h2_y]):
        for px_near, py_near in zip([p_x,p_x,p_x-1,p_x+1],[p_y+1,p_y-1,p_y,p_y]): # up,down,left,right
            if px_near==h_x and py_near==h_y:
                hunter_near_num+=1
                break
            else:
                continue
        if hunter_near_num==2:
            print('-----CATCHED-----')
            return True
        else:
            # print('-----MISSED-----')   # it was ignoreing
            return False

def make_plot(fig, x_list, y_list, frame_num):
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

def check_edge(move_way_list, position, edge_len):
    if position[0]==0:
        move_way_list.remove('left')
    elif position[0]==edge_len-1:
        move_way_list.remove('right')
    if position[1]==0:
        move_way_list.remove('down')
    elif position[1]==edge_len-1:
        move_way_list.remove('up')

    return move_way_list

def counter(steps, param=10000):
    if steps % param==0:
        print(f'STEPS  :  {steps}')

def print_debug(hunter_1, hunter_2, prey, edge_len, is_debug=False, is_Q=False):
    # params for printing
    print_str = False

    if not is_debug:
        pass
    else:
        if print_str:
            print(f'HUNTER_1 POSITION  :  {hunter_1.position}')
            print(f'HUNTER_2 POSITION  :  {hunter_2.position}')
            print(f'PREY     POSITION  :  {prey.position}')
        else:
            white = np.zeros((edge_len, edge_len))
            white[hunter_1.position[0]][hunter_1.position[1]] = 1
            white[hunter_2.position[0]][hunter_2.position[1]] = 2
            white[prey.position[0]][prey.position[1]] = 3
            print(white)
        
    if is_Q:
        print(hunter_1.Q)



def set_another_agent(hunter_1, hunter_2, prey):
    hunter_1.another_hunter = hunter_2
    hunter_2.another_hunter = hunter_1
    prey.hunter_1 = hunter_1
    prey.hunter_2 = hunter_2

def update_position(position, move_way):
    new_x, new_y = position
    if move_way=='up':
        new_y += 1
    elif move_way=='down':
        new_y -= 1
    elif move_way=='left':
        new_x -= 1
    elif move_way=='right':
        new_x += 1
    else:
        print('\nWRONG WAY ARE CHOSEN\n')
        raise ValueError

    new_position = [new_x, new_y]
    return new_position