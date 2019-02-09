import random

#######################################################
## Environment (class)                               ##
## Models and administrates the environment / states ##
## and manages the time discrete updates             ##
#######################################################

class Environment:
     """
    Variabels
    ----------
    self.trash_grid : ndarray
         Numpy array (dimension is chosen in init function) that stores where trash is

    self.agent_grid : ndarray
        Numpy array (dimension is chosen in init function) that stores where the different agents are

    self.agents : list
        Stores all the numbers of actual agents

    self.history_agent_grids : list
        List of the n last agent_grids

    self.history_visible_trash_grids: list
        List of the n last tash_grids

    self.dim : tuple
        Dimension of the Grids (trash and agent grid use this size)

    ----------
    """

    def __init__(self, dim):

    """Initial function for the environment.

    Called to set up all basic things for the environment.
    Parameters
    ----------
    dim : int tuple
        Dimension of the field.

    Returns
    -------

    """
        self.dim = dim # (y,x)
        # initialize trash grid
        self.trash_grid = np.zeros(self.dim[0], self.dim[1])
        # initialize robot grid
        self.agent_grid = np.zeros(self.dim[0], self.dim[1])

        # History is the list of grids seen over time
        self.history_agent_grids = []
        self.history_visible_trash_grids = []

        # Keep track of all agents
        self.agents = []

    # Getter Methods
    def get_agent_position(self, id):
        # agents id is equivalent to its index in the agents list
        return agents[id].pos

    def get_agent(self, agent_idx):
        return agents[agent_idx]

    def is_position_free_valid(self, coord):
        """Checks if a field is free so that an agent can move/appear there.
            a field is free and valid if it is inside the grid and there is
            no robot on the field.

        ----------
        coord : int tuple / None
            Coordinates where the new agent should appear (place in the grid has to
            be free that the agent appears there) . And has to be valid
        return
        -------
        bool
            Is True when the agent could appear on the passed coordinates and if the coordinates are valid
            and false if not

        """

        if((0 <= coord[0] and coord[0] < self.dim[0])  and (0 <= coord[1] and coord[1] < self.dim[1]) and (self.agent_grid(coord) == 0)):
            # Valid and free coordinate
            return True
        # At coord no agent could appear / move to
        return False


    def compute_visible_trash_grid():
        """ Computes the intersection of the current trash grid and current
        agent grid. Has ones whereever a agent floats over some trash

                TODO
        """

    def get_trash_grid():
        return self.trash_grid

    def get_agent_grid():
        return self.agent_grid

    def get_rnd_free_position(self):
        """
         Returns a coordinate of the grid that is currently not occupied
         by any agent.
         If no free coordinate was found an exception is raised

         return
         -------
         tuple int:
            If there is a free position (random 100 tries), this is returned as tuple
        """
        count_tries = 0
        while count_tries < 100:
            coord_y = random.randint(0,self.dim[0])
            coord_x = random.randint(0,self.dim[1])
            if self.is_position_free_valid((coord_y,coord_x)):
                return (coord_y,coord_x)
            count_tries += 1

        raise Exception("No free coordinate found")



    def add_agent(self, coord = None, capacity=10):
        """Initial function for the environment.

        Called to set up all basic things for the environment.
        Parameters
        ----------
        coord : int tuple / None
            Coordinates where the new agent should appear (place in the grid has to
            be free that the agent appears there).
        capacity: int
            Default is 10. Defines how much the agent could carry

        -------

        """
        succesfully_added = False
        exception_caught = False
        if coord is None:
            try:
                coord = get_rnd_free_position()
            except Exception:
                print("Handled exception")
                exception_caught = True

        else if not self.is_position_free_valid(coord):
            print("Can not add agent at this position")
            exception_caught = True

        if exception_caught:
            return False

        id = len(self.agents)
        # Add agent to list and grid
        self.agents.append(Agent(pos = coord, id = id, capacity = capacity))
        self.agent_grid[coord] = id
        return True




    def move_agent(agent_idx, delta_coords):
        """
        If possible the agent at given index, which is currently at a position
        pos will move to the position pos + delta_coords
        returns True if the move was succesfully performed
        returns False if the move wasn't valid and therefore not performed
        """


        # Check move for validity
        old_pos = self.agents[agent_idx].pos
        new_pos = old_pos + delta_coords
        if is_position_free_valid(new_pos):
            # Update the and agents position
            agent_id = self.agents[agent_idx].id
            self.agents[agent_idx].pos = new_pos
            self.agent_grid[new_pos] = agent_id
            self.agent_grid[old_pos] = 0

            # If the robot sees some trash --> reward
            # Trash removal
            # All trash treatments TODO

            # Return reward!



    def move_agents(self, action_list):
        """Updates the environment with the actions in the list.

        Conversion from the action into the actual change of coordinate (check if this action is possible
        is in self.move_agent)

        Returns the
        Parameters
        ----------
        action_list : list
            Containing the actions for each agent (0: up, 1: right, 2: down, 3 left)
            Agents are ordered as in the self.agents list.
            Dimension: 1 x Number of agents
        -------
        """
        agent_idx = 0
        reward_list = []
        for action in action_list:
            conversion_action_coord = {0:[-1,0], 1: [0,1], 2:[1,0], 3:[0,1]}
            d_pos = conversion_action_coord[action]
            reward_list.append(self.move_agent(agent_idx, d_pos))
            agent_idx = agent_idx + 1
            #TODO GIVING back reward or not



        # for all agents (sequential action performance):
            # check validity of predicted action
            # if valid perform action and update grids,agents etc.

    def estimate_q(position_agent, ):
        # call neural net ->


    def check_action(agent_id,pos_origin, pos_predicted):
        # Returns bool (possibility of action as well as the Reward )
        return possible, reward


        #numpy array n_agents x grid_height x grid_widht X (n_number_timesteps x Channel (own_position (one_hot_vector), other_position (one_hot_vector), garbish)
    def export_known_data():
        """Exports the .

        Conversion from the action into the actual change of coordinate (check if this action is possible
        is in self.move_agent)

        Parameters
        ----------
        action_list : list
            Containing the actions for each agent (0: up, 1: right, 2: down, 3 left)
            Agents are ordered as in the self.agents list.
            Dimension: 1 x Number of agents
        -------
        """
