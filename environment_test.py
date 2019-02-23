"""
Script to test the environment
"""

import Environment
import numpy as np
def simulated_get_actions(seed_value=0, number_created_agents=1):
    """ Simulates the function which

    """
    #Returns a random actions list for each robot
    np.random.seed(seed_value)
    action_list = list(np.random.randint(low=0, high=5, size=number_created_agents))
    print(action_list)


    return action_list

#Test variables
NUMBER_AGENTS = 1
CAPACITY_PER_AGENT = 10
NUMBER_SIMULATED_STEPS = 100
DIM = (4, 4)
REWARD_EAT_TRASH = 1 #Default is 1 
REWARD_INVALID_MOVE = -1 #Default is -1 
REWARD_NOTHING_HAPPEND = 0 #Default is 0
TRASH_APPEARENCE_PROB = 1 #Default is 0.1 
NUMBER_TRASH_SOURCES = 4  #Default is 4
SAVED_TIMESTEPS = 3 

#Print statements
PRINT_OVERVIEW_AGENTS = False
PRINT_HISTORY = True
PRINT_TRASH_HISTORY = True 
PRINT_HISTORY_AGENTS = False
PRINT_EACH_AGENTS_VIEW = True
PRINT_COMPLETE_TRASH = True 
PRINT_REWARD_LIST = True

#Create an environment with the dimensionality dim

test_environment = Environment.Environment(dim=DIM, reward_eat_trash=REWARD_EAT_TRASH, reward_invalid_move=REWARD_EAT_TRASH,
 reward_nothing_happend=REWARD_NOTHING_HAPPEND, trash_appearence_prob=TRASH_APPEARENCE_PROB, 
 number_trash_sources=NUMBER_TRASH_SOURCES, saved_timesteps=SAVED_TIMESTEPS)


number_created_agents = 0
#Add the agents
for i in range(0, NUMBER_AGENTS):
    if(test_environment.add_agent(coord=None, capacity=CAPACITY_PER_AGENT)):
        print("Agent {} is created succesfully".format(i))
        number_created_agents += 1
    else:
        print("Agent {} isn't created".format(i))


for step in range(0, NUMBER_SIMULATED_STEPS):
    print("{}. step started".format(step))
    history_visible_trash, history_agents, current_pos_agent, trash_grid_complete, trash_sources = test_environment.debug_data_export()
    if(PRINT_OVERVIEW_AGENTS):
        print("Current overview of all agents:\n {}".format(history_agents[-1]))
    if(PRINT_HISTORY):
        if(PRINT_TRASH_HISTORY):
            print("History visible trash : {}".format(history_visible_trash))
        if(PRINT_HISTORY_AGENTS):
            print("History Agents {}".format(history_agents))
    if(PRINT_EACH_AGENTS_VIEW):
        print("Current Pos Agents:\n {}".format(current_pos_agent))
    if(PRINT_COMPLETE_TRASH):
        print("Complete Trash Distribution:\n {}".format(trash_grid_complete))
    action_list=simulated_get_actions(seed_value=step, number_created_agents=number_created_agents)
    print("Make the actions {}".format(action_list))
    history_visible_trash, history_agents, current_pos_agent, reward_list = test_environment.move_agents(action_list)
    if(PRINT_REWARD_LIST):
        print("The reward list for the current actions:\n{}".format(reward_list))
    