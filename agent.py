class Agent:

    def __init__(self, pos, id, capacity):
        self.pos = pos
        self.id = id
        # maximum amount of trash the agent is capable to carry
        self.capacity = capacity
        # current load of trash carried by this agent
        self.load = 0
        # total amount of trash collected over time
        self.totally_collected = 0
