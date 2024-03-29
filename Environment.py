import random
import numpy as np
from Motion import Motion
from  GaussianTrashSource import GaussianTrashSource
from Agent import Agent
#####################################################
# Environment (class)                               #
# Models and administrates the environment / states #
# and manages the time discrete updates             #
#####################################################

EMPTY_TILE_ID = 0 #Defines the value assigned to a tile in self.agent_grid if there is no agent on a field




class Environment:
    """
    Variabels
    ----------
    self.trash_grid_complete : ndarray
         Numpy array (dimension is chosen in init function) that stores where trash is

    self.trash_grid_visible : ndarray
         Numpy array (dimension is chosen in init function) that stores where currently trash AND agents are

    self.agent_grid : ndarray
        Numpy array (dimension is chosen in init function) that stores where
        the different agents are

    self.agents : list
        Stores all the numbers of actual agents

    self.history_agent_grids : list
        List of the n last agent_grids

    self.history_visible_trash_grids: list
        List of the n last tash_grids

    self.dim : tuple
        Dimension of the Grids (trash and agent grid use this size)

    self.trash_sources : list
        List of Trashsources who can generate some trash each round.
    ----------

    """


    def __init__(self, dim, reward_eat_trash=10, reward_invalid_move=0, reward_nothing_happend=0, trash_appearence_prob=0.1, number_trash_sources=1, saved_timesteps=1):
        """Initial function for the environment.

        Called to set up all basic things for the environment.
        Parameters
        ----------
        dim : int tuple
        Dimension of the field.

        Returns
        -------

        """
        #Important Parameter initialization
        self.saved_timesteps = saved_timesteps # Number of timesteps saved for the neural network
        self.dim = dim # (y,x)

        # Constants that will be used all throughout the code

        self.REWARD_EAT_TRASH = reward_eat_trash #Default is 1
        self.REWARD_INVALID_MOVE = reward_invalid_move #Default is -1
        self.REWARD_NOTHING_HAPPEND = reward_nothing_happend #Default is 0
        self.TRASH_APPEARENCE_PROB = trash_appearence_prob #Default is 0.1
        self.NUMBER_TRASH_SOURCES = number_trash_sources  #Default is 4
        # initialize trash grid
        self.trash_grid_visible = np.zeros(shape=(self.dim[0], self.dim[1]), dtype=int)
        self.trash_grid_complete = np.zeros(shape=(self.dim[0], self.dim[1]), dtype=int)

        # initialize robot grid
        self.agent_grid = np.zeros(shape=(self.dim[0], self.dim[1]), dtype=int) * EMPTY_TILE_ID

        # History is the list of grids seen over time, first element is the oldest one,
        # last element in the list is the newest one, for the initialisation they are filled
        # up with empty grids
        self.history_agent_grids = []
        self.history_visible_trash_grids = []
        # Create some random trash sources
        self.trash_sources = []
        for i in range(self.NUMBER_TRASH_SOURCES):
            self.trash_sources.append(self.create_random_trash_source())
        # Keep track of all agents
        self.agents = []
        self.number_agents_total = 0 #Number of every created agents (even if they have been deleted)
        for timestep_counter in range(0, self.saved_timesteps):
            self.history_agent_grids.append(self.agent_grid)
            self.history_visible_trash_grids.append(self.trash_grid_visible)


    # Getter Methods
    def get_agent_position(self, id):
        # agents id is equivalent to its index in the agents list
        return self.agents[id].pos

    def get_agent(self, agent_idx):
        return self.agents[agent_idx]

    def is_position_free_valid(self, coord):
        """
        Checks if a field is free so that an agent can move/appear there.
        a field is free and valid if it is inside the grid and there is
        no robot on the field.
        
        Parameters
        ----------
        coord : int tuple / None
            Coordinates where the new agent should appear (place in the grid
            has to be free that the agent appears there) . And has to be valid
        
        return
        -------
        bool
            Is True when the agent could appear on the passed coordinates and
            if the coordinates are valid and false if not
        """
        if((0 <= coord[0] and coord[0] < self.dim[0])  and (0 <= coord[1] and coord[1] < self.dim[1]) and (self.agent_grid[coord] == EMPTY_TILE_ID)):
            # Valid and free coordinate
            return True
        # At coord no agent could appear / move to
        return False

    def get_complete_trash_grid(self):
        return self.trash_grid_complete

    def get_agent_grid(self):
        return self.agent_grid

    def get_rnd_free_position(self):
        """
         Returns a coordinate of the grid that is currently not occupied
         by any agent.
         If no free coordinate was found an exception is raised. To find a free
         coordinate it tries randomly for 100 times if there is a free spot. 

         return
         -------
         tuple int:
            If there is a free position, this is returned as tuple
        """
        count_tries = 0
        while count_tries < 100:
            coord_y = random.randint(0, self.dim[0])
            coord_x = random.randint(0, self.dim[1])
            if self.is_position_free_valid((coord_y, coord_x)):
                return (coord_y, coord_x)
            count_tries += 1

        raise Exception("No free coordinate found")

    def add_agent(self, coord=None, capacity=10):
        """Initial function for the environment.

        Called to set up all basic things for the environment.
        Parameters
        ----------
        coord : int tuple / None
            Coordinates where the new agent should appear (place in the grid has to
            be free that the agent appears there). Succesful created agents will have an idea 
            that correspondend to the number of already created agents. 
        capacity: int
            Default is 10. Defines how much the agent could carry

        Return
        -------
        bool:
            Returns if adding the agent was succesful. 

        """
        exception_caught = False
        if coord is None:
            try:
                coord = self.get_rnd_free_position()
            except Exception:
                print("Handled exception")
                exception_caught = True

        elif not self.is_position_free_valid(coord):
            print("Can not add agent at this position")
            exception_caught = True

        if exception_caught:
            return False
        #TODO:  see Issue #4

        id = self.number_agents_total +1 #Every Agent has the ID of Agents that have been created before  +1 (doesn't get reduced if the agents are removed, first Agent ID is 1)
        self.number_agents_total += 1 #Update the number of agents which have ever been created
        # Add agent to list and grid
        self.agents.append(Agent(pos=coord, id=id, capacity=capacity))
        self.agent_grid[coord] = id
        return True

    def move_agent(self, agent_idx, delta_coords):
        """
        - Moves agent (if move is valid)
        - Eats trash if there is some on the new position.
        - Returns the Reward that is collected with this move (e.g. eat trash)
        
        Parameters
        ----------
        agent_idx : int tuple
            ID of the agent.
        delta_coords: int tuple
            Defines how the y,x coordinates should change
        
        Return 
        -------
        int: 
            Amount of collected reward with this move
        """

        # Check move for validity
        my_agent = self.agents[agent_idx]
        old_pos = my_agent.pos
        new_pos = (old_pos[0] + delta_coords[0], old_pos[1] + delta_coords[1])
        wants_to_move = (delta_coords[0] != 0) or (delta_coords[1] != 0)
        reward = 0

        # Does the robot see trash on the new position?
        self.trash_grid_visible[old_pos] = 0 #Resets the Visible Trash Grid on the old position

        if self.is_position_free_valid(new_pos) or not wants_to_move:
            # TODO: See issue #5
            # Update the agents position
            my_agent.pos = new_pos
            self.agent_grid[old_pos] = EMPTY_TILE_ID
            self.agent_grid[new_pos] = my_agent.id

            # Trash eating
            trash_eaten = self.move_agent_in_trash_world(old_pos = old_pos, new_pos = new_pos, my_agent = my_agent)
            if trash_eaten:
                reward = self.REWARD_EAT_TRASH
        else:
            # TODO: See issue #6
            # Invalid move
            reward = self.REWARD_INVALID_MOVE

        return reward

    def move_agent_in_trash_world(self, old_pos, new_pos, my_agent):
        """
        Called from move_agent() to move an agent from old_pos to new_pos.
        Applies the agents move (old_pos -> new_pos) to the "trash world".
        Updates all trash related attributes, trash_grids etc.
        Returns True if the agent eats trash at new_pos
        
        Parameters
        ----------
        old_pos : int tuple 
            y,x coordinate of the old position.
        new_pos: int tuple
            y,x coordinate of the agent after the move (could be the same as of old position if the move is invalid or stay)
        my_agent: Agent object
            The instance of the Agent that should be moved
        
        Return 
        -------
        int: 
            Amount of trash that have been eaten
        """

        
        trash_eaten = False
        trash_present = self.trash_grid_complete[new_pos] > 0
        # Eat trash if there is some
        if trash_present:
            # visible only stores whether there is currently an agent collecting trash
            self.trash_grid_visible[new_pos] = 1
            # complete stores the amount of trash present
            self.trash_grid_complete[new_pos] -= 1
            my_agent.load += 1
            my_agent.totally_collected += 1
            trash_eaten = True
        else:
            self.trash_grid_visible[new_pos] = 0

        return trash_eaten

    def create_random_trash_source(self):
        """
        Creates a Trashsource with a random position on the grid.
        The trash source is NOT automatically added somewhere!

        Return 
        -------
        GaussianTrashSource: 
            Returns the create Trashsource as an instance of the GaussianTrashSource class
        """
        mean_x = random.randint(0, self.dim[1]-1)
        mean_y = random.randint(0, self.dim[0]-1)
        mean = [mean_y,mean_x]
        return GaussianTrashSource(mean=mean, max_y=self.dim[0]-1, max_x=self.dim[1]-1, cov = [[0,0],[0,0]])


    def generate_new_trash(self, alpha=None):
        """
        Each trashsource of the environment is, with probability alpha,
        asked to generate a piece of trash that will then appear on the grid.
        New trash will be added to the trash_grid_complete

        Parameters
        ----------
        alpha : float / None 
            Probability for each Trash Source to generate Trash. If alpha is None the 
            self.TRASH_APPEARENCE_PROB probability is used. 
        """
        
        if alpha is None:
            alpha = self.TRASH_APPEARENCE_PROB

        for source in self.trash_sources:
            if random.random() < alpha:
                trash_y, trash_x = source.get_trash()
                self.trash_grid_complete[trash_y, trash_x] += 1


    def move_agents(self, action_list):
        """Updates the environment with the actions in the list.

        Conversion from the action into the actual change of coordinate (check
        if this action is possible is in self.move_agent)

        Returns the current state that is used by the neural net as well as the rewards
        collected by the moves of the action_list

        Parameters
        ----------
        action_list : list
            Containing the actions for each agent (0: up, 1: right, 2: down, 3: left, 4: stay)
            Agents are ordered as in the self.agents list.
            Dimension: 1 x Number of agents
        Return
        -------
        ndarray: 
            History over the visible trash, for each saved timestep. (Dimension: grid_height x grid_width x saved_timesteps)
        
        ndarray:

        """
        agent_idx = 0
        reward_list = []
        for action in action_list:
            d_pos = Motion(action).value
            reward_list.append(self.move_agent(agent_idx, d_pos))
            agent_idx = agent_idx + 1

        self.generate_new_trash()
        # Save the current conditions (Stempeluhr) as next Timestep
        self.save_condition_new_timestep()
        history_visible_trash, history_agents, current_pos_agent = self.export_known_data()

        # numpy array n_agents x grid_height x grid_widht X (n_number_timesteps x Channel (own_position (one_hot_vector), other_position (one_hot_vector), garbish)
        return history_visible_trash, history_agents, current_pos_agent, reward_list


        #numpy array n_agents x grid_height x grid_widht X (n_number_timesteps x Channel (own_position (one_hot_vector), other_position (one_hot_vector), garbish)
    def save_condition_new_timestep(self):
        """Adds the current condition to the state space and removes the oldest one
            Saves the agent_grid and the trash_grid_visible matrix
        """
        #Add the new ones

        self.history_agent_grids.append(self.agent_grid.copy())
        self.history_visible_trash_grids.append(self.trash_grid_visible.copy()) #Only the visible trash is saved

        # remove the oldest appended data
        del(self.history_agent_grids[0])
        del(self.history_visible_trash_grids[0])

    def export_known_data(self):
        """Exports the data (states) to the neural network.

        n: number of saved timesteps
        Return
        -------
            history_visible_trash:
                Matrix of format n * self.dim[0] * self.dim[1], is 1 where trash is eaten at each timestep, zero elsewhere

            history_agent:
                Matrix of format n* self.dim[0] * self.dim[1], is 1 where the agents are at one timestep, zero elsewhere

            current_pos_agent:
                Matrix of format nb_agents * self.dim[0] * self.dim[1], one hot matrix for each agent (in the same order as the agents are in self.agents)
                indicating the position of the agent
        """
        ret_history_visible_trash_grids = np.array(self.history_visible_trash_grids)
        ret_history_visible_trash_grids[ret_history_visible_trash_grids>0] = 1 # 1 indicates trash, 0 elsewhere

        ret_history_agents = np.array(self.history_agent_grids)
        ret_history_agents[ret_history_agents > 0] = 1  # 1 indicates an agent, 0 if there is no agent

        current_pos_agent = np.zeros((len(self.agents), self.dim[0], self.dim[1]), dtype = int)
        #Iterating over the list of agents to set the position of each agent in another field to 1
        agent_counter = 0
        for agent in self.agents:
            y, x = agent.pos[0], agent.pos[1]
            current_pos_agent[agent_counter][y][x] = 1
            agent_counter += 1
        return ret_history_visible_trash_grids, ret_history_agents, current_pos_agent

    def debug_data_export(self):
        """Exports all data of the current stats for debug reasons. Extends the export_known_data_function with complete_trash_grid

        n: number of saved timesteps
        Return
        -------
            history_visible_trash:
                Matrix of format n * self.dim[0] * self.dim[1], is 1 where trash is eaten at each timestep, zero elsewhere

            history_agent:
                Matrix of format n* self.dim[0] * self.dim[1], is 1 where the agents are at one timestep, zero elsewhere

            current_pos_agent:
                Matrix of format nb_agents * self.dim[0] * self.dim[1], one hot matrix for each agent (in the same order as the agents are in self.agents)
                indicating the position of the agent

            trash_grid_complete:
                Matrix of format self.dim[0] * self.dim[1]. Indicates the complete (partly for the agents unknown) distribution of trash
            
            trash_sources: 
                List of all TrashShource Objects that are generating currently trash. 
        """
        ret_history_visible_trash_grids, ret_history_agents, current_pos_agent = self.export_known_data()
        return ret_history_visible_trash_grids, ret_history_agents, current_pos_agent , self.trash_grid_complete ,self.trash_sources
