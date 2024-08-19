from Board import Board



class State(Board):
    def __init__(self):
        pass

class Node(object):

    def __init__(self):
        self.parent = None
        self.children = []

        self.visit_times = 0
        self.total_value = 0.0

        self.state = None

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

    def set_visit_times(self, times):
        self.visit_times = times

    def visit_times_add_one(self):
        self.visit_times += 1

    def get_total_value(self):
        return self.total_value

    def set_total_value(self, value):
        self.total_value = value

    def add_total_value(self, n):
        self.total_value += n

    def is_all_expand(self):
        return len(self.children) == AVAILABLE_CHOICE_NUMBER

    def add_child(self, sub_node):
        sub_node.set_parent(self)
        self.children.append(sub_node)


def UCTSearch():
    pass

def TreePolicy():
    pass

def Expand():
    pass

def BestChild():
    pass

def DefaultPolicy():
    pass

def BackUp():
    pass
