class Board:
    def __init__(self,width, height, WinCount):
        self.width = width
        self.height = height
        self.WinCount = WinCount
        self.board = []
        for i in range(0, height):
            line = []
            for j in range(0, width):
                line.append(-1)
            self.board.append(line)

    class WinnerChecker:
        def __init__(self, winCount):
            self.winner = -1
            self.curCount = 0
            self.winCount = winCount

        def clear(self):
            self.winner = -1
            self.curCount = 0

        def next_pos(self, id):
            if id != self.winner:
                self.winner = id
                self.curCount = 1
            else:
                self.curCount += 1
                if self.winner != -1 and self.curCount >= self.winCount:
                    return True
            return False


    def has_winner(self):
        checker = self.WinnerChecker(self.WinCount)
        # 判断行上的最长连续
        for i in range(0, self.height):
            checker.clear()
            for j in range(0, self.width):
                if checker.next_pos(self.board[i][j]):
                    return True, checker.winner
        # 判断列上的最长连续
        for j in range(0, self.width):
            checker.clear()
            for i in range(0, self.height):
                if checker.next_pos(self.board[i][j]):
                    return True, checker.winner
        # 主对角线上的最长连续
        for i in range(0, self.height):
            x = i
            y = 0
            checker.clear()
            while x < self.height and y < self.width:
                if checker.next_pos(self.board[x][y]):
                    return True, checker.winner
                x += 1
                y += 1
        for i in range(1, self.width):
            x = 0
            y = i
            checker.clear()
            while x < self.height and y < self.width:
                if checker.next_pos(self.board[x][y]):
                    return True, checker.winner
                x += 1
                y += 1

        # 副对角线上的最长连续
        for i in range(0, self.height):
            x = i
            y = 0
            checker.clear()
            while x >= 0 and y < self.width:
                if checker.next_pos(self.board[x][y]):
                    return True, checker.winner
                x -= 1
                y += 1
        for i in range(1, self.width):
            x = self.height - 1
            y = i
            checker.clear()
            while x >= 0 and y < self.width:
                if checker.next_pos(self.board[x][y]):
                    return True, checker.winner
                x -= 1
                y += 1

        return False, None