from tkinter import messagebox
from Agent.Player import Player
from Board import Board
from GameView import GameView

class Game(Board):

    def __init__(self, width, height, WinCount):
        Board.__init__(self,width,height,WinCount)
        self.player = []
        self.player.append(Player("p1",self))
        self.player.append(Player("p2",self))
        self.curPlayer = 0  # 修正为从0开始
        self.gameView = GameView(self)




    def game_play(self):
        while True:
            x, y = self.player[self.curPlayer].getInput()  # 从当前玩家获取输入
            self.board[y][x] = self.curPlayer
            self.gameView.draw_piece(x, y, self.curPlayer)
            winner, player = self.has_winner()
            if winner:
                messagebox.showinfo("游戏结束", f"玩家 {player + 1} 获胜!")
                break
            self.curPlayer ^= 1  # 切换玩家
        self.gameView.root.quit()