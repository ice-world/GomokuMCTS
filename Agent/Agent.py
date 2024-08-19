from abc import abstractmethod


class Agent:
    def __init__(self,name):
        self.name = name

    @abstractmethod
    def getInput(self):
        pass