from Agent.Agent import Agent

from MCTS import *


class AI(Agent):
    def __init__(self, name, game, id):
        Agent.__init__(self, name=name)
        self.game = game
        self.id = id

    def getInput(self):
        node = Node()
        state = State(self.game.width, self.game.height, self.game.WinCount, self.id, self.id)
        state.board =  copy.deepcopy(self.game.board)
        state.ComputeAvailableChoices()
        node.set_state(state)
        best = MCTS(node)
        return best.x, best.y
