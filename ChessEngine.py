import numpy as np


"""
This class is responsible for storing all the information about the current state of the chess game, as well
as determining the valid moves at the current state. It will also keep a move log
"""
from copy import deepcopy
#using numpy arrays would make it more efficient for the AI engine, but for just 2 players this is just fine
class GameState():
    def __init__(self): #think of this as the constructor
        #board is 8x8 2D list, where each element of the list has two characters.
        #first character represents colour of the piece, b or w
        #second character represents type of the piece "K", "Q", "R", "B", "N" or "p"
        #"--" represents empty space with no piece
        self.board = [  #this is the field board. It will be called to create the board on ChessMain
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove = True #this field will determine whose term it is
        self.moveLog = [] #field to keep a move log. Important for castling
        self.scoreLog = [0] #material score log
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () #coordinates for the square where the enpassant capture is possible
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

        self.dic = {}
        self.dic["wp"] = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [50, 50, 50, 50, 50, 50, 50, 50],
                           [10, 10, 20, 30, 30, 20, 10, 10],
                           [5, 5, 10, 25, 25, 10, 5, 5],
                           [0, 0, 0, 20, 20, 0, 0, 0],
                           [5, -5, -10, 0, 0, -10, -5, 5],
                           [5, 10, 10, -20, -20, 10, 10, 5],
                           [0, 0, 0, 0, 0, 0, 0, 0]]
        self.dic["bp"] = np.negative(list(reversed(self.dic["wp"])))
        self.dic["wN"] = [[-50,-40,-30,-30,-30,-30,-40,-50],
                                [-40,-20,  0,  0,  0,  0,-20,-40],
                                [-30,  0, 10, 15, 15, 10,  0,-30],
                                [-30,  5, 15, 20, 20, 15,  5,-30],
                                [-30,  0, 15, 20, 20, 15,  0,-30],
                                [-30,  5, 10, 15, 15, 10,  5,-30],
                                [-40,-20,  0,  5,  5,  0,-20,-40],
                                [-50,-40,-30,-30,-30,-30,-40,-50]]
        self.dic["bN"] = np.negative(list(reversed(self.dic["wN"])))
        self.dic["wB"] = [[-20,-10,-10,-10,-10,-10,-10,-20],
                                [-10,  0,  0,  0,  0,  0,  0,-10],
                                [-10,  0,  5, 10, 10,  5,  0,-10],
                                [-10,  5,  5, 10, 10,  5,  5,-10],
                                [-10,  0, 10, 10, 10, 10,  0,-10],
                                [-10, 10, 10, 10, 10, 10, 10,-10],
                                [-10,  5,  0,  0,  0,  0,  5,-10],
                                [-20,-10,-10,-10,-10,-10,-10,-20]]
        self.dic["bB"] = np.negative(list(reversed(self.dic["wB"])))
        self.dic["wR"] = [[0,  0,  0,  0,  0,  0,  0,  0],
                              [5, 10, 10, 10, 10, 10, 10,  5],
                             [-5,  0,  0,  0,  0,  0,  0, -5],
                             [-5,  0,  0,  0,  0,  0,  0, -5],
                             [-5,  0,  0,  0,  0,  0,  0, -5],
                             [-5,  0,  0,  0,  0,  0,  0, -5],
                             [-5,  0,  0,  0,  0,  0,  0, -5],
                              [0,  0,  0,  5,  5,  0,  0,  0]]
        self.dic["bR"] = np.negative(list(reversed(self.dic["wR"])))
        self.dic["wQ"] = [[-20,-10,-10, -5, -5,-10,-10,-20],
                            [-10,  0,  0,  0,  0,  0,  0,-10],
                            [-10,  0,  5,  5,  5,  5,  0,-10],
                             [-5,  0,  5,  5,  5,  5,  0, -5],
                              [0,  0,  5,  5,  5,  5,  0, -5],
                            [-10,  5,  5,  5,  5,  5,  0,-10],
                            [-10,  0,  5,  0,  0,  0,  0,-10],
                            [-20,-10,-10, -5, -5,-10,-10,-20]]
        self.dic["bQ"] = np.negative(list(reversed(self.dic["wQ"])))


        self.wKingTableSG = [[-30,-40,-40,-50,-50,-40,-40,-30],
                            [-30,-40,-40,-50,-50,-40,-40,-30],
                            [-30,-40,-40,-50,-50,-40,-40,-30],
                            [-30,-40,-40,-50,-50,-40,-40,-30],
                            [-20,-30,-30,-40,-40,-30,-30,-20],
                            [-10,-20,-20,-20,-20,-20,-20,-10],
                             [20, 20,  0,  0,  0,  0, 20, 20],
                             [20, 30, 10,  0,  0, 10, 30, 20]]

        self.wKingTableEG = [[-50,-40,-30,-20,-20,-30,-40,-50],  ##TODO: add this for endgames
                                [-30,-20,-10,  0,  0,-10,-20,-30],
                                [-30,-10, 20, 30, 30, 20,-10,-30],
                                [-30,-10, 30, 40, 40, 30,-10,-30],
                                [-30,-10, 30, 40, 40, 30,-10,-30],
                                [-30,-10, 20, 30, 30, 20,-10,-30],
                                [-30,-30,  0,  0,  0,  0,-30,-30],
                                [-50,-30,-30,-30,-30,-30,-30,-50]]
        self.bKingTableEG = np.negative(list(reversed(self.wKingTableEG)))

        self.dic["wK"] = self.wKingTableSG
        self.dic["bK"] = np.negative(list(reversed(self.dic["wK"])))

        self.pieces = {"bR":2, "bN":2, "bB":2, "bQ":1, "bK":1, "bp":8,
                    "wR":2, "wN":2, "wB":2, "wQ":1, "wK":1, "wp":8}

    def minimax(self,depth, alpha, beta, whiteToMove):

        if depth == 0:
            validMoves = self.getValidMoves()
            evaluation = self.evalPosition(validMoves)
            return [evaluation]
        if whiteToMove:
            maxEval = -9999999
            counter = -1
            moves = self.getValidMoves()
            for move in moves:
                counter += 1
                self.makeMove(move)
                eval = self.minimax(depth - 1, alpha, beta, self.whiteToMove)[0]
                if eval > maxEval:
                    maxEval = eval
                    moveIndex = counter
                alpha = max(alpha, eval)
                if beta <= alpha:
                    self.undoMove()
                    break
                self.undoMove()

            return [maxEval, moves[moveIndex]]
        else:
            minEval = 9999999
            counter = -1
            moves = self.getValidMoves()
            for move in moves:
                counter +=1
                self.makeMove(move)
                eval = self.minimax(depth - 1, alpha, beta, self.whiteToMove)[0]
                if eval < minEval:
                    minEval = eval
                    moveIndex = counter
                beta = min(beta, eval)
                if beta <= alpha:
                    self.undoMove()
                    break
                self.undoMove()

            return [minEval, moves[moveIndex]]


    def evalPosition(self,validMoves): ##TODO: instead of scanning the dic every time, start with score = 0 and substract (or add) after captures
        ##TODO also need to remove after undoing ; use .pop()
        ## TODO pawn promotion
        # print(self.scoreLog)
        # if self.moveLog[-1].pieceCaptured != "--":
        #     score = self.scoreLog[-1]
        #     piece = self.moveLog[-1].pieceCaptured
        #     if piece[0] == "w":
        #         sign = -1
        #     else:
        #         sign = 1
        #     if piece[1] == "R":
        #         score += sign*500
        #     elif piece[1] == "N":
        #         score += sign*320
        #     elif piece[1] == "B":
        #         score += sign*330
        #     elif piece[1] == "Q":
        #         score += sign*900
        #     elif piece[1] == "p":
        #         score += sign*100
        #     self.scoreLog.append(score)
        #     print(self.scoreLog)
        # if len(validMoves) == 0:
        #     if self.whiteToMove == True:
        #         evaluation = -900000
        #     else:
        #         evaluation = 900000
        # else:
        #     evaluation = self.scoreLog[-1] + self.doubledPawns() + self.piecesPositions()
        #
        # return evaluation

        pieces = self.pieces #get all the pieces on the board
        listPieces = list(pieces.keys()) #list of individual pieces still playing
        points = {} #initiate empty dictionary with the points each piece has
        if len(validMoves) != 0: #check is the move results in checkmate
            for key in listPieces:
                if key[0] == "b": #white maximizes and black minimizes
                    sign = -1
                else:
                    sign = 1

                if key[1] == "R": #assign score given a piece type
                    points[key] = sign * pieces[key] * 500
                elif key[1] == "N":
                    points[key] = sign * pieces[key] * 320
                elif key[1] == "B":
                    points[key] = sign * pieces[key] * 330
                elif key[1] == "Q":
                    points[key] = sign * pieces[key] * 900
                elif key[1] == "K":
                    points[key] = sign * pieces[key] * 20000
                elif key[1] == "p":
                    points[key] = sign * pieces[key] * 100

            evaluation = sum(points.values()) + self.doubledPawns() + self.piecesPositions()

        else:
            if self.whiteToMove == True:
                evaluation = -900000
            else:
                evaluation = 900000

        return evaluation



    def doubledPawns(self):
        score = 0
        for cols in range(0, 8):
            bPawnsInCol = 0
            wPawnsInCol = 0
            bPawnsBlocked = 0
            wPawnsBlocked = 0
            for rows in range(0,8):
                piece = self.board[rows][cols]
                if piece[1] == "p" and piece[0] == "w":
                    wPawnsInCol += 1
                    if self.board[rows-1][cols] != "--":
                        wPawnsBlocked += 1
                elif piece[1] == "p" and piece[0] == "b":
                    bPawnsInCol += 1
                    if self.board[rows+1][cols] != "--":
                        bPawnsBlocked += 1
            if wPawnsInCol > 0:
                score = score - (wPawnsInCol - 1) * 50
            if bPawnsInCol > 0:
                score = score + (bPawnsInCol - 1) * 50
            score = score + (-wPawnsBlocked + bPawnsBlocked) * 10

        return score

    def piecesPositions(self): #score based on position of each piece
        score = 0

        for rows in range(0, 8):
            for cols in range(0, 8):
                piece = self.board[rows][cols]

                if piece != "--":
                    score = score + self.dic[piece][rows][cols]

        return score


    def makeMove(self, move):
        """
        What does the function do in order to move a piece? it takes a piece given the initial coordinates and
        sets it in the new coordinates
        We don't need to worry about the capture pieces since these will be stored in the pieceCaptured
        variable
        We don't need to worry about validating the moves at the moment, since we will have something generating
        a list of all valid moves and only allows the user to make those valid moves
        This function alone won't work for castling, pawn promotion and en-passant.
        """
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        if self.moveLog[-1].pieceCaptured != "--":
            self.pieces[self.moveLog[-1].pieceCaptured] -=1



        self.whiteToMove = not self.whiteToMove #swap players after each move

        #update the king's location if needed
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"
            if move.pieceMoved[0] == "w":
                self.pieces["wQ"] +=1
            else:
                self.pieces["bQ"] +=1

        #en passant capture
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--" #capturing the pawn

        #update enpassantPossible variable
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

        #castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = "--" #erase rook
            else: #queen side castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]  # moves rook into new square
                self.board[move.endRow][move.endCol - 2] = "--"  # erase rook

        #update castling rights - whenever it is a rook or a king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))


    """
    Undo the last move made
    """
    def undoMove(self):
        if len(self.moveLog) != 0: #make sure that there is a move to undo

            if self.moveLog[-1].pieceCaptured != "--":
                # print(self.moveLog[-1].pieceCaptured)
                # self.scoreLog.pop()
                self.pieces[self.moveLog[-1].pieceCaptured] += 1
            if self.moveLog[-1].isPawnPromotion: #remove the extra queen from the pieces dictionary
                if self.moveLog[-1].pieceMoved[0] == "w":
                    self.pieces["wQ"] -= 1
                else:
                    self.pieces["bQ"] -= 1
            move = self.moveLog.pop() #remove from the log
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured #Undo move
            self.whiteToMove = not self.whiteToMove #swap players
            #update king's position if needed
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            #undo enpassant move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--" #leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            #undo a 2 square pawn advance
            if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            #undo castling rights
            self.castleRightsLog.pop() #get rid of the new castling rights from the move we are undoing
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            #undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"
                else: #queenside
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"


    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.bks = False


    """
    All moves considering checks
    self.getCastleMoves(r, c, moves, allyColor)
    """
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs) #copy the current castling rights
        #1) Generate all possible moves
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        #2) for each move, make the move
        for i in range(len(moves)-1, -1, -1): #better to remove items backwards
            self.makeMove(moves[i])
            #3) generate all oponents moves
            #4) for each of those moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove #switch turns
            if self.inCheck():
                moves.remove(moves[i]) #5) if they attack your king, it's not a valid move
            self.whiteToMove = not self.whiteToMove  # switch turns
            self.undoMove() #this will also swap the term. We just need to make sure that we do it an even number of times
        if len(moves) == 0: #either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves

    """
    Determine if the current player is under check
    """
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    """
    Determine if the enemy can attack the square r, c
    """
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opponents view
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #if square is under attack
                return True
        return False




    """
    All moves without considering checks
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of columns in given rows
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #call the appropiate move function based on piece type

        return moves


    """
    Get all the pawn moves for the pawn located at row, col and add those moves to the list
    First check if the sq in front of the pawn
    """
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawns moves
            if self.board[r-1][c] == "--": #check if the sq in front is empty
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #check if 2 sqs in front is empty
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: #captures to the left
                if self.board[r - 1][c - 1][0] == "b": #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))
            if c+1 <= 7: #captures to the right
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))
        else: #black pawns
            if self.board[r + 1][c] == "--":  # check if the sq in front is empty
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # check if 2 sqs in front is empty
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # captures to the left
                if self.board[r + 1][c - 1][0] == "w":  # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))
            if c + 1 <= 7:  # captures to the right
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))
        #add pawn promotions later
    """
    Get all the rook moves for the pawn located at row, col and add those moves to the list
    """
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy color valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else:
                    break


    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy color valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    """
    Generate all valid castling moves for the king at (r, c) and add them to the list of moves
    """
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return #can't castle while in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)

    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove = True))


    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))


class CastleRights():
    def __init__ (self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    # """
    # Now we can either use a chess or coordinate notation. We choose chess notation since it just makes it more
    # intuitive. For this, we will need to use a dictionary which maps o-7 to 1-8 and A-H and viceversa.
    # """
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()} #very cool way to reverse a dictionary
    filesToCols = {"A": 0, "B": 1, "C": 2, "D": 3,
                   "E": 4, "F": 5, "G": 6, "H": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}



    # What defines a move? A start square, an end square, the current board state (to validate the move).
    # We are just storing the move log and the current snapshot of the board, not all the snapshots of the board
    # We need the snapshot of the board in order to undo the capture of pieces

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #the above is just to store the moves and captures, not moving.
        self.isPawnPromotion = False
        if (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7):
            self.isPawnPromotion = True
        #en passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"
        #castle move
        self.isCastleMove = isCastleMove
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    def getChessNotation(self): #get the position in (almost real) chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


    """
    Overriding the equals method
    """
    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False




