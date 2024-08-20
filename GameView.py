

import tkinter as tk
from Agent.Player import Player


class GameView:
    def __init__(self,game):
        # 初始化Tkinter窗口
        self.game = game
        self.root = tk.Tk()
        self.root.title("五子棋")
        self.cell_size = 30  # 每个格子的大小
        self.canvas = tk.Canvas(self.root, width=self.game.width * self.cell_size, height=self.game.height * self.cell_size)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)  # 绑定鼠标点击事件

        self.draw_board()  # 绘制棋盘

    def draw_piece(self, x, y, player):
        """在棋盘上绘制一颗棋子"""
        x0 = x * self.cell_size + 2
        y0 = y * self.cell_size + 2
        x1 = x0 + self.cell_size - 4
        y1 = y0 + self.cell_size - 4
        color = "black" if player == 0 else "white"
        self.canvas.create_oval(x0, y0, x1, y1, fill=color)
    def draw_board(self):
        """绘制棋盘的网格线"""
        for i in range(self.game.width):
            for j in range(self.game.height):
                x0 = i * self.cell_size
                y0 = j * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")


    def on_click(self, event):
        """处理鼠标点击事件"""
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if x < self.game.width and y < self.game.height and self.game.board[x][y] == -1:
            print(self.game.player[self.game.curPlayer].name)
            if isinstance(self.game.player[self.game.curPlayer],Player):
                self.game.player[self.game.curPlayer].setInput(x, y)
