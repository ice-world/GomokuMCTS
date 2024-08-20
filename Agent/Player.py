from Agent.Agent import Agent


class Player(Agent):
    def __init__(self, name, game):
        Agent.__init__(self,name=name)
        self.game = game
        self.input_ready = False
        self.input_x = -1
        self.input_y = -1

    def getInput(self):
        """等待用户点击并返回点击的坐标"""
        self.input_ready = False
        while not self.input_ready:
            print("wating update")
            self.game.gameView.root.update()  # 更新Tkinter的事件循环以接收点击事件
        return self.input_x, self.input_y

    def setInput(self, x, y):
        """设置用户输入的坐标"""
        self.input_x = x
        self.input_y = y
        self.input_ready = True
