
from Hunter import Hunter
from Prey import Prey
import utils
import numpy as np
from tqdm import tqdm
import cv2

# "agp" means all agent's place
# 0,0 of agp is left_below

def main(episodes, alpha=0.1, gannma=0.9, epsilon=0.1, edge_len=25, prj_name=None):
    # assertion
    assert episodes >= 100, ('EPISODES ARE DEFINED AS TO BE MORE THAN 99 !!')
    assert prj_name is not None, ('SET PROJECT NAME !!')
    # log
    logger = utils.make_logger(prj_name)
    # initialize
    prey = Prey(edge_len)
    hunter_1, hunter_2 = Hunter(alpha,gannma,epsilon,edge_len,prey,logger), Hunter(alpha,gannma,epsilon,edge_len,prey,logger)
    utils.set_another_agent(hunter_1, hunter_2, prey)

    steps_list = []
    save_path = f'./plot_data/{prj_name}_E{episodes}_L{edge_len}.png'

    # learning
    for episode in tqdm(range(episodes)):

        # initialize till position correctly
        while True:
            hunter_1.initialize_position()
            hunter_2.initialize_position()
            prey.initialize_position()
            if hunter_1.position == hunter_2.position or hunter_1.position==prey.position or hunter_2.position==prey.position:
                pass
            else:
                # print(f'HUNTER_1 STARTS AT {hunter_1.position}')
                # print(f'HUNTER_2 STARTS AT {hunter_2.position}')
                # print(f'PREY     STARTS AT {prey.position}')
                break
        
        # repetetion
        steps = 0
        while True:
            steps += 1
            hunter_1.check_25()
            hunter_2.check_25()

            hunter_1_catched = hunter_1.update_Q()
            # check Q after hunter_1 update
            if hunter_1_catched:break

            hunter_2_catched = hunter_2.update_Q()
            # check Q after hunter_2 update
            if hunter_2_catched:break

            prey.move()
            prey_catched = utils.catched(hunter_1.position, hunter_2.position, prey_position=prey.position)
            # check Q after prey update
            if prey_catched:break

            # print per param
            utils.counter(steps, param=10000)
            utils.print_debug(hunter_1, hunter_2, prey, edge_len, logger, is_debug=True, is_Q=False)
        
        # steps per episode
        steps_list.append(steps)
    
    # plotting
    plot_graph = utils.make_plot([e for e in range(1, episodes+1)], steps_list)
    cv2.imwrite(save_path, plot_graph)


if __name__=='__main__':
    main(episodes=1000, edge_len=10, prj_name='test_20')