"""
Script to test the environment 
"""

import environment
import numpy as np 
def simulated_get_actions(seed_value = 0, number_created_agents = 1):
    #Returns a random actions list for each robot
    np.random.seed(seed_value)
    action_list = list(np.random.randint(low = 0, high = 5,size = number_created_agents))
    print(action_list)


    return action_list

#Test variables 
number_agents = 16
capacity_per_agent = 10
number_simulated_steps = 5

#Print statements 
print_history = False
print_each_agents_view = True

#Create an environment with the dimensionality dim  
dim = (4,4)
test_environment  = environment.Environment(dim = dim )
number_created_agents = 0
#Add the agents 
for i in range(0, number_agents): 
    if(test_environment.add_agent(coord = None, capacity= capacity_per_agent)):
        print("Agent {} is created succesfully".format(i))
        number_created_agents += 1
    else: 
        print("Agent {} isn't created".format(i))


for step in range(0,number_simulated_steps):
    print("{}. step started".format(step))
    history_visible_trash, history_agents, current_pos_agent = test_environment.export_known_data()
    #print("Known data of the environment:")
    print("Current Overview all agents")
    print("{}".format(history_agents[-1]))
    if(print_history):
        print("History visible trash : {}".format(history_visible_trash))
        print("History Agents {}".format(history_agents))
    if(print_each_agents_view):
        print("Current Pos Agents:\n {}".format(current_pos_agent))
    action_list = simulated_get_actions(seed_value= step, number_created_agents= number_created_agents)
    print("Make the actions {}".format(action_list))
    history_visible_trash, history_agents, current_pos_agent, reward_list = test_environment.move_agents(action_list)

    #print("{}. step finished".format(step))