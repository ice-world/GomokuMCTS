import copy
import math
import random

from Board import Board


class State(Board):
    def __init__(self, width, height, win_count, current_player, controller):
        Board.__init__(self, width, height, win_count)
        self.value = 0
        self.current_player = current_player
        self.available_choices = []
        self.available_choices_count = -1
        self.controller = controller

    def IsTerminal(self):
        win, winner = self.has_winner()
        if win:
            if winner == self.controller:
                self.value = 100000
            else:
                self.value = -100000
        if self.available_choices_count == -1:
            self.ComputeAvailableChoices()
        if self.available_choices_count == 0:
            self.value = 0.01
            return True
        return win

    def GetCurrentValue(self):
        return self.value

    def ComputeValue(self):
        if self.value == 0:
            self.IsTerminal()
        return self.value

    def ComputeAvailableChoices(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.board[i][j] == -1:
                    self.available_choices.append((i, j))
        self.available_choices_count = len(self.available_choices)

    def RandomComputeNextState(self):
        if self.available_choices_count == 0:
            self.ComputeAvailableChoices()
        next_state = State(self.width, self.height, self.WinCount, self.current_player ^ 1, self.controller)
        x, y = random.choice(self.available_choices)
        next_state.board = copy.deepcopy(self.board)
        next_state.board[x][y] = self.current_player
        next_state.IsTerminal()
        return next_state, x, y


class Node(object):

    def __init__(self):
        self.parent = None
        self.children = []

        self.visit_times = 0
        self.total_value = 0.0

        self.state = None
        self.x = 0
        self.y = 0

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_children(self):
        return self.children

    def get_visit_times(self):
        return self.visit_times

    def visit_times_add_one(self):
        self.visit_times += 1

    def get_total_value(self):
        return self.total_value

    def add_total_value(self, n):
        self.total_value += n

    def is_all_expand(self):
        return len(self.children) == self.get_state().available_choices_count

    def add_child(self, sub_node):
        sub_node.set_parent(self)
        self.children.append(sub_node)


def UCTSearch():
    pass


def TreePolicy(node):
    nextNode = None
    while not node.state.IsTerminal():
        if node.is_all_expand():
            node = BestChild(node, True)
        else:
            nextNode = Expand(node)
            return nextNode
    return node

def Expand(node):
    tried_sub_node_states = [
        sub_node.get_state() for sub_node in node.get_children()
    ]
    next_state, x, y = node.get_state().RandomComputeNextState()
    while next_state in tried_sub_node_states:
        next_state, x, y = node.get_state().RandomComputeNextState

    sub_node = Node()
    sub_node.x = x
    sub_node.y = y
    sub_node.set_state(next_state)
    node.add_child(sub_node)

    return sub_node


def BestChild(node, IsExploration):
    bestScore = float("-inf")
    bestSubNode = None

    for subNode in node.get_children():
        if IsExploration:
            C = 1.0 / math.sqrt(2.0)
        else:
            C = 0.0
        score = subNode.get_total_value() + C * math.sqrt(
            2.0 * math.log(node.get_visit_times() / subNode.get_visit_times()))
        if score > bestScore:
            bestScore = score
            bestSubNode = subNode
    return bestSubNode


def DefaultPolicy(node):
    current_state = node.get_state()
    #print("DefaultPolicy is running")
    while not current_state.IsTerminal():
        current_state ,x,y= current_state.RandomComputeNextState()

    final_state_reward = current_state.ComputeValue()
    return final_state_reward


def BackUp(node, reward):
    while node is not None:
        node.visit_times_add_one()
        node.add_total_value(reward)
        node = node.parent


def MCTS(node):
    computationBudget = 2000

    for i in range(computationBudget):
        print("MCTS is running")
        expendNode = TreePolicy(node)

        reward = DefaultPolicy(expendNode)

        BackUp(expendNode, reward)
    best_next_node = BestChild(node, False)

    return best_next_node
'''
def main():
    node = Node()
    state = State(7, 7, 5, 0)
    node.set_state(state)
    MCTS(node)
'''