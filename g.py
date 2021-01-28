def makeMove2(self, move):
    self.board2 = deepcopy(self.board)

    self.board2[move.startRow][move.startCol] = "--"
    self.board2[move.endRow][move.endCol] = move.pieceMoved

