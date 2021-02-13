from model import *
from game import *
from view import Agent

class Brain:
    """
    a brain, human or AI
    """

    def __init__(self, agent):
        """
        agent (Agent): the agent
        """
        pass

    def request_move(self):
        return self.agent.request_move()
