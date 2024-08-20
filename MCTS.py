import copy
import math
import random
import sys

from Board import Board


class State(Board):
    def __init__(self, width, height, win_count, current_player, controller):
        Board.__init__(self, width, height, win_count)
        self.value = 0
        self.current_player = current_player
        self.available_choices = []
        self.available_choices_count = -1
        self.controller = controller

    def is_connected(self, x, y):
        dir = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        for dx, dy in dir:
            nx = x + dx
            ny = y + dy
            if nx < 0 or nx >= self.height or ny < 0 or ny >= self.width:
                continue
            if self.board[nx][ny] != -1:
                return True
        return False

    def connected_count(self):
        checker = self.WinnerChecker(sys.maxsize)
        connected_num = []
        for i in range(0, max(self.width, self.height) + 1):
            connected_num.append(0)
        # 判断行上的最长连续
        for i in range(0, self.height):
            checker.clear()
            for j in range(0, self.width):
                checker.next_pos(self.board[i][j])
                if checker.winner == self.controller:
                    connected_num[checker.curCount] += 1
                elif checker.winner == self.controller ^ 1:
                    connected_num[checker.curCount] -= 10
        # 判断列上的最长连续
        for j in range(0, self.width):
            checker.clear()
            for i in range(0, self.height):
                checker.next_pos(self.board[i][j])
                if checker.winner == self.controller:
                    connected_num[checker.curCount] += 1
                elif checker.winner == self.controller ^ 1:
                    connected_num[checker.curCount] -= 10
        # 主对角线上的最长连续
        for i in range(0, self.height):
            x = i
            y = 0
            checker.clear()
            while x < self.height and y < self.width:
                checker.next_pos(self.board[x][y])
                if checker.winner == self.controller:
                    connected_num[checker.curCount] += 1
                elif checker.winner == self.controller ^ 1:
                    connected_num[checker.curCount] -= 10
                x += 1
                y += 1
        for i in range(1, self.width):
            x = 0
            y = i
            checker.clear()
            while x < self.height and y < self.width:
                checker.next_pos(self.board[x][y])
                if checker.winner == self.controller:
                    connected_num[checker.curCount] += 1
                elif checker.winner == self.controller ^ 1:
                    connected_num[checker.curCount] -= 10
                x += 1
                y += 1

        # 副对角线上的最长连续
        for i in range(0, self.height):
            x = i
            y = 0
            checker.clear()
            while x >= 0 and y < self.width:
                checker.next_pos(self.board[x][y])
                if checker.winner == self.controller:
                    connected_num[checker.curCount] += 1
                elif checker.winner == self.controller ^ 1:
                    connected_num[checker.curCount] -= 10
                x -= 1
                y += 1
        for i in range(1, self.width):
            x = self.height - 1
            y = i
            checker.clear()
            while x >= 0 and y < self.width:
                checker.next_pos(self.board[x][y])
                if checker.winner == self.controller:
                    connected_num[checker.curCount] += 1
                elif checker.winner == self.controller ^ 1:
                    connected_num[checker.curCount] -= 10
                x -= 1
                y += 1

        return connected_num

    def IsTerminal(self):
        win, winner = self.has_winner()
        if self.available_choices_count == -1:
            self.ComputeAvailableChoices()
        if self.available_choices_count == 0:
            return True
        return win

    def GetCurrentValue(self):
        return self.value

    def state_evaluate(self):
        count = self.connected_count()
        value = 0.0
        mul = 1
        for i in count:
            value += mul * i
            mul *= 10
        return value

    def ComputeValue(self):
        '''
        count = self.connected_count()
        value = 0.0
        mul = 1
        for i in count:
            value += mul * i
            mul *= 10
        '''
        value = 0
        win, winner = self.has_winner()
        if win:
            if winner == self.controller:
                value = 1000000
            else:
                value = -1000000
        self.value = value
        return self.value

    def ComputeAvailableChoices(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.board[i][j] == -1 and self.is_connected(i, j):
                    self.available_choices.append((i, j))
        self.available_choices_count = len(self.available_choices)

    def RandomComputeNextState(self):
        if self.available_choices_count == -1:
            self.ComputeAvailableChoices()
        next_state = State(self.width, self.height, self.WinCount, self.current_player ^ 1, self.controller)
        x, y = random.choice(self.available_choices)
        next_state.board = copy.deepcopy(self.board)
        next_state.board[x][y] = self.current_player
        return next_state, x, y

    def simple_compute_next_state(self):
        best_state = None
        best_score = 0
        if self.current_player != self.controller:
            best_score = float("inf")
        else:
            best_score = float("-inf")
        best_x = 0
        best_y = 0
        if self.available_choices_count == -1:
            self.ComputeAvailableChoices()
        next_state = State(self.width, self.height, self.WinCount, self.current_player ^ 1, self.controller)
        next_state.board = copy.deepcopy(self.board)
        for x, y in self.available_choices:
            next_state.board[x][y] = self.current_player
            score = next_state.state_evaluate()
            if self.current_player != self.controller:
                if score < best_score:
                    best_state = copy.deepcopy(next_state)
                    best_score = score
                    best_x = x
                    best_y = y
            else:
                if score > best_score:
                    best_state = copy.deepcopy(next_state)
                    best_score = score
                    best_x = x
                    best_y = y
            next_state.board[x][y] = -1
        return best_state, best_x, best_y


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
    # print("DefaultPolicy is running")
    while not current_state.IsTerminal():
        current_state, x, y = current_state.simple_compute_next_state()

    final_state_reward = current_state.ComputeValue()
    return final_state_reward


def BackUp(node, reward):
    while node is not None:
        node.visit_times_add_one()
        node.add_total_value(reward)
        node = node.parent


def MCTS(node):
    computationBudget = 1000

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
