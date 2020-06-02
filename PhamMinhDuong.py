# -*- coding: utf-8 -*-
"""
Pham Minh Duong - 51702081
"""
from tkinter import *
import math
import time

class BoardError(Exception):
    def __init__(self, value):
        self.__value = value
        
    def __str__(self):
        return repr(self.__value)

class GameError(Exception):
    def __init__(self, value):
        self.__value = value
        
    def __str__(self):
        return repr(self.__value)

class Board:
    
    EMPTY = 0    
    X = 1
    O = 2
    CHARS = [" ", "X", "O"]
    
    def __init__(self, height, width):
        """
            Create a board with defined height and width
            Fill 0 (empty) to every cell of the board
        """
        self.__height = height
        self.__width = width
        self.__cells = []
        for i in range(height):
            self.__cells.append([])
            for j in range(width):
                self.__cells[i].append(Board.EMPTY)
    
        
    def draw(self):
        """
            Sketch the board
        """
        s = "-"
        for j in range(self.__width):
            s += "--"
        s += "\n"
        for i in range(self.__height):
            s += "|"
            for j in range(self.__width):
                s += str(Board.CHARS[self.__cells[i][j]]) + "|"
            s += "\n-"
            for j in range(self.__width):
                s += "--"
            s += "\n"
        return s
        
    def getHeight(self):
        """
            Get height of self
        """
        return self.__height
    
    def getWidth(self):
        """
            Get width of self
        """
        return self.__width
    
    def getBoardStatus(self):
        """
            Return the status of all the cells (a list of list of int)
        """
        return self.__cells
    
    def setBoardStatus(self, cells):
        """
            Override the current status of the board by value of cell
        """
        self.__cells = cells

    def getCellStatus(self, cell):
        """
            Check status of the cell
        """
        return self.__cells[cell[0]][cell[1]]
    
    def isEmptyCell(self, cell):
        """
            Check if the cell is empty
        """
        if self.__cells[cell[0]][cell[1]] == 0:
            return True
        return False
    
    def mark(self, value, cell):
        """
            Mark value to cell
        """
        self.__cells[cell[0]][cell[1]] = value 
    
    def getEmptyCells(self):
        """
            Return coordinates of all empty_cells
        """
        emptycells = []
        for i in range(self.__height):
            for j in range(self.__width):
                cell = (i,j)
                if self.isEmptyCell(cell):
                    emptycells.append(cell)
        return emptycells
                
    def isNeighbors(self,cell1,cell2):
        if cell1[0] == cell2[0]:
            if cell1[1] in [cell2[1]-1,cell2[1]+1]:
                return True
            return False
        elif cell1[1] == cell2[1]:
            if cell1[0] in [cell2[0]-1,cell2[0]+1]:
                return True
            return False
        else: 
            if (cell1[1] in [cell2[1]-1,cell2[1]+1]) and (cell1[0] in [cell2[0]-1,cell2[0]+1]):
                return True
            return False
        
    def getNeighbors(self, cell):
        """
            Return neighbors of a cell
        """
        neighborcells = []
        for i in range(self.__height):
            for j in range(self.__width):
                cellother = (i,j)
                if self.isNeighbors(cell,cellother):
                    neighborcells.append(cellother)
        return neighborcells

class Game:
    
    ACTIVE = 1
    INACTIVE = 0
    NOWINNER = -1
    TIE = 0
    X = 1
    O = 2
    HUMAN = 1
    MACHINE = 2 
    
    def __init__(self, height, width, firstTurn, winNumber):
        """
            Begin a game and define which attributes are necessary to describe the game status at some moment
        """
        self.__winNumber = winNumber
        self.__board = Board(height, width)
        self.__turn = firstTurn
        self.__status = Game.ACTIVE
        self.__winner = Game.NOWINNER
    
    def getCellBounds(self,row, col):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid 
        global CELL_SIZE
        
        x0 = col * CELL_SIZE + 5
        x1 = (col+1) * CELL_SIZE + 5
        y0 = row * CELL_SIZE + 5
        y1 = (row+1) * CELL_SIZE + 5
        return (x0, y0, x1, y1)
    
    def drawBoard(self,canvas):
        board = self.getBoard()
        for row in range(board.getHeight()):
            for col in range(board.getWidth()):
                (x0, y0, x1, y1) = self.getCellBounds(row, col)
#                fill = "orange" if (data.selection == (row, col)) else "cyan"
                canvas.create_rectangle(x0, y0, x1, y1, fill="cyan")
#        print (self.getBoard().draw())
    
    def mousePressed(self,event):
        if(self.getTurn() == self.HUMAN):
            (row, col) = self.getCell(event.x, event.y)
            self.mark((row,col))
        else:
            print("Please wait machine")
    
    def drawChess (self,canvas,cell,fill):
        (x0,y0,x1,y1) = self.getCellBounds(cell [0], cell[1])
        
        locationChessX0 = (x0 +x1)/2 - CELL_SIZE /2
        locationChessY0 = (y0 + y1)/2 - CELL_SIZE /2
        locationChessX1 = (x0 +x1)/2 + CELL_SIZE /2
        locationChessY1 = (y0 + y1)/2 + CELL_SIZE /2
        canvas.create_oval(locationChessX0,
                       locationChessY0,
                       locationChessX1,
                       locationChessY1, fill=fill)
    
    def pointInGrid(self,x, y):
        global canvasWidth, canvasHeight
    # return True if (x, y) is inside the grid defined by data.
        return ((5 <= x <= canvasWidth-5) and (5 <= y <= canvasHeight-5))
    
    def getCell(self,x,y):
        if (not self.pointInGrid(x, y)):
            return
        row = (y - 5) // CELL_SIZE
        col = (x - 5) // CELL_SIZE
        # triple-check that we are in bounds
        row = min(self.getBoard().getHeight()-1, max(0, row))
        col = min(self.getBoard().getWidth()-1, max(0, col))
        return (row, col)
    
    def getBoard(self):
        
        return self.__board

    def isActive(self):
        """
            Get if the game is still active
        """
        if self.__status == 1:
            return True
        return False   
    
    def getTurn(self):
        """
            Get whose's turn next
        """
        if self.isActive():
            return self.__turn
    

    
    def getWinner(self):
        """
            Get winner
        """
        return self.__winner
        
    def getWinNumber(self):
        """
            Get the winNumber
        """
        return self.__winNumber
    
    def deactivate(self):
        """
            If the game is active, deactivate it
        """
        if self.isActive():
            self.__status = self.INACTIVE
        else:
            deactivateErr = GameError("The game is INACTIVED").__str__()
            print(deactivateErr)
    
    def activate(self):
        """
            If the game is inactive, activate it
        """
        if not self.isActive():
            self.__status = self.ACTIVE
        else:
            activateErr = GameError("The game is ACTIVED").__str__()
            print(activateErr)
            
        
    def switchTurn(self):
        """
            Change the turn to the other player
        """
        if self.__turn == 1:
            self.__turn = 2
            return;
        self.__turn = 1
    
    def declareWinner(self, player):
        """
            Declare a winner
        """
        self.__winner = player

    def mark(self, cell):
        global canvas,MINIMAX_DEPTH
        if self.isActive() and self.getTurn() == self.HUMAN and self.getBoard().isEmptyCell(cell):
            self.getBoard().mark(1,cell)
            fill = "black"
            self.drawChess(canvas,cell,fill)
            
            board = self.getBoard().getBoardStatus()
            winner = self.checkWinner(board)
            self.switchTurn()
            if winner == 1:
                self.declareWinner(winner)
                print("HUMAN win!")
                self.deactivate()
                return
            
            aiMove = self.find_next_move_forAI(board, MINIMAX_DEPTH)
                
            if not aiMove:
                print("Ai can not find possible moves")
                print("TIED!")
                self.deactivate()
                
            fill = "white"
            self.getBoard().mark(2,(aiMove[0],aiMove[1]))
            self.drawChess(canvas,(aiMove[0],aiMove[1]),fill)
            self.switchTurn()
            
            winner = self.checkWinner(board)
            if winner == 2:
                self.declareWinner(winner)
                print("MACHINE win!")
                self.deactivate()
                self.switchTurn()
                return
                
            if len(self.generateMoves(board)) == 0:
                print("No possible moves left!")
                print("TIED!")
                self.deactivate()
            
        else:
            if not self.isActive():
                raise GameError("Game has finished!")
            if self.getTurn() != self.HUMAN:
                strErr = "It's not HUMAN 's turn!"
                raise GameError(strErr)
            if not self.getBoard().isEmptyCell(cell):
                strErr = "Cell " + str(cell) + " is not empty!"
                raise GameError(strErr)

    def getConsecutiveSetScore(self,count, prevents, currentTurn):
        global winScore
        winGuarantee = 1000000
    
        if prevents == 2 and count < 5:
            return 0
    
        if count == 5:
            return winScore
        elif count == 4:
            if currentTurn:
                return winGuarantee
            else:
                if prevents == 0:
                    return winGuarantee/4
                else:
                    return 200
        elif count == 3:
            if prevents == 0:
                if currentTurn:
                    return 50000
                else:
                    return 200
            else:
                if currentTurn:
                    return 10
                else:
                    return 5
        elif count == 2:
            if prevents == 0:
                if currentTurn:
                    return 7
                else:
                    return 5
            else:
                return 3
        elif count == 1:
            return 1
    
        return winScore*2

    def evaluateHorizontal(self,boardMatrix, isHuman, humanTurn ):
        consecutive = 0
        prevents = 2
        score = 0
        for i in range(len(boardMatrix)):
            for j in range(len(boardMatrix[0])):
                if (isHuman and boardMatrix[i][j] == 1) or (not isHuman and boardMatrix[i][j] == 2):
                    consecutive = consecutive + 1
                elif boardMatrix[i][j] == 0:
                    if consecutive > 0:
                        prevents = prevents - 1
                        score += self.getConsecutiveSetScore(consecutive, prevents, isHuman == humanTurn)
                        consecutive = 0
                        prevents = 1
                    else:
                        prevents = 1
                elif consecutive > 0:
                    score += self.getConsecutiveSetScore(consecutive, prevents, isHuman == humanTurn)
                    consecutive = 0
                    prevents = 2
                else:
                    prevents = 2
    
            if consecutive > 0:
                score += self.getConsecutiveSetScore(consecutive, prevents, isHuman == humanTurn)
    
            consecutive = 0
            prevents = 2
    
        return score

    def evaluateVertical(self,boardMatrix, isHuman, humanTurn ):
        consecutive = 0
        prevents = 2
        score = 0
    
        for j in range(len(boardMatrix[0])):
            for i in range(len(boardMatrix)):
                if (isHuman and boardMatrix[i][j] == 1) or (not isHuman and boardMatrix[i][j] == 2):
                    consecutive = consecutive + 1
                elif boardMatrix[i][j] == 0:
                    if consecutive > 0:
                        prevents = prevents - 1
                        score += self.getConsecutiveSetScore(consecutive, prevents, isHuman == humanTurn)
                        consecutive = 0
                        prevents = 1
                    else:
                        prevents = 1
                elif consecutive > 0:
                    score += self.getConsecutiveSetScore(consecutive, prevents, isHuman == humanTurn)
                    consecutive = 0
                    prevents = 2
                else:
                    prevents = 2
    
            if consecutive > 0:
                score += self.getConsecutiveSetScore(consecutive, prevents, isHuman == humanTurn)
    
            consecutive = 0
            prevents = 2
    
        return score
    
    def evaluateDiagonal(self,boardMatrix, isHuman, humanTurn ):
        consecutive = 0
        prevents = 2
        score = 0
    
        # From bottom-left to top-right diagonally
        for k in range(0, 2 * (len(boardMatrix) - 1) + 1):
            iStart = max(0, k - len(boardMatrix) + 1)
            iEnd = min(len(boardMatrix) - 1, k)
            for i in range(iStart, iEnd + 1):
                j = k - i
                
                if (isHuman and boardMatrix[i][j] == 1) or (not isHuman and boardMatrix[i][j] == 2):
                    consecutive = consecutive + 1
                elif boardMatrix[i][j] == 0:
                    if consecutive > 0:
                        prevents = prevents - 1
                        score += self.getConsecutiveSetScore(consecutive, prevents, isHuman == humanTurn)
                        consecutive = 0
                        prevents = 1
                    else:
                        prevents = 1
                elif consecutive > 0:
                    score += self.getConsecutiveSetScore(consecutive, prevents, isHuman == humanTurn)
                    consecutive = 0
                    prevents = 2
                else:
                    prevents = 2
    
            if consecutive > 0:
                score += self.getConsecutiveSetScore(consecutive, prevents, isHuman == humanTurn)
    
            consecutive = 0
            prevents = 2
    
        # From top-left to bottom-right diagonally
        for k in range(1-len(boardMatrix), len(boardMatrix)):
            iStart = max(0, k)
            iEnd = min(len(boardMatrix) + k - 1, len(boardMatrix)-1)
            for i in range(iStart, iEnd + 1):
                j = i - k
                
                if (isHuman and boardMatrix[i][j] == 1) or (not isHuman and boardMatrix[i][j] == 2):
                    consecutive = consecutive + 1
                elif boardMatrix[i][j] == 0:
                    if consecutive > 0:
                        prevents = prevents - 1
                        score += self.getConsecutiveSetScore(consecutive, prevents, isHuman == humanTurn)
                        consecutive = 0
                        prevents = 1
                    else:
                        prevents = 1
                elif consecutive > 0:
                    score += self.getConsecutiveSetScore(consecutive, prevents, isHuman == humanTurn)
                    consecutive = 0
                    prevents = 2
                else:
                    prevents = 2
    
            if consecutive > 0:
                score += self.getConsecutiveSetScore(consecutive, prevents, isHuman == humanTurn)
    
            consecutive = 0
            prevents = 2
    
        return score
    
    def generateMoves(self,boardMatrix):
        moveList = []
        boardSize = len(boardMatrix)
        # Look for cells that has at least one stone in an adjacent cell.
        for i in range(boardSize):
            # print(boardMatrix[i])
            for j in range(boardSize):
                
                if boardMatrix[i][j] == 1 or boardMatrix[i][j] == 2:
                    continue
                
                if i > 0:
                    if j > 0:
                        if (boardMatrix[i-1][j-1] == 1 or boardMatrix[i-1][j-1] == 2) or ((boardMatrix[i][j-1] == 1 or boardMatrix[i][j-1] == 2)):
                            move = [i,j]
                            moveList.append(move)
                            continue
                    if j < boardSize-1:
                        if (boardMatrix[i-1][j+1] == 1 or boardMatrix[i-1][j+1] == 2) or (boardMatrix[i][j+1] == 1 or boardMatrix[i][j+1] == 2):
                            move = [i,j]
                            moveList.append(move)
                            continue
                    if boardMatrix[i-1][j] == 1 or boardMatrix[i-1][j] == 2:
                        move = [i,j]
                        moveList.append(move)
                        continue
                    
                if i < boardSize-1:
                    if j > 0:
                        if (boardMatrix[i+1][j-1] == 1 or boardMatrix[i+1][j-1] == 2) or (boardMatrix[i][j-1] == 1 or boardMatrix[i][j-1] == 2):
                            move = [i,j]
                            moveList.append(move)
                            continue
                    if j < boardSize-1:
                        if (boardMatrix[i+1][j+1] == 1 or boardMatrix[i+1][j+1] == 2) or (boardMatrix[i][j+1] == 1 or boardMatrix[i][j+1] == 2):
                            move = [i,j]
                            moveList.append(move)
                            continue
                    if boardMatrix[i+1][j] == 1 or boardMatrix[i+1][j] == 2:
                        move = [i,j]
                        moveList.append(move)
                        continue

        return moveList
    
    def getScore(self,boardMatrix, isHuman, humanTurn):
        
        return self.evaluateHorizontal(boardMatrix, isHuman, humanTurn) + self.evaluateVertical(boardMatrix, isHuman, humanTurn) + self.evaluateDiagonal(boardMatrix, isHuman, humanTurn)
    
    def checkWinner(self,boardMatrix):
        global winScore
        
        if self.getScore(boardMatrix, True, False) >= winScore:
            return 1
    
        if self.getScore(boardMatrix, False, True) >= winScore:
            return 2
        return 0
    
    def addStoneNoGUI(self,boardMatrix, posX, posY, isHuman):
        tmpBoardMatrix = []
        for i in range(20):
            tmpBoardMatrix.append([])
            for j in range(20):
                tmpBoardMatrix[i].append(Board.EMPTY)
    
        for i in range(20):
            for j in range(20):
                tmpBoardMatrix[i][j] = boardMatrix[i][j]
    
    
        if isHuman:
            tmpBoardMatrix[posY][posX] = 1
        else:
            tmpBoardMatrix[posY][posX] = 2
    
        return tmpBoardMatrix
    
    def searchWinningMove(self,boardMatrix):
        global winScore
        
        allPossibleMoves = self.generateMoves(boardMatrix)
        winningMove = []
        
        # Iterate for all possible moves
        for move in allPossibleMoves:
            # Play the move to that temporary board without drawing anything
            tmpBoardMatrix = self.addStoneNoGUI(boardMatrix, move[1], move[0], False)
            
            # If the bot player has a winning score in that temporary board, return the move.
            if self.getScore(tmpBoardMatrix, False, False) >= winScore:
                winningMove.append(move[0])
                winningMove.append(move[1])
                return winningMove
            
        return None
    
    def calculateScoreRate(self,boardMatrix, isHumanTurn):
        humanScore = self.getScore(boardMatrix, True, isHumanTurn)
        botScore = self.getScore(boardMatrix, False, isHumanTurn)
        if humanScore == 0:
            humanScore = 1.0
        
        return botScore / humanScore
    
    def minimax_AB(self,depth, boardMatrix, is_max, alpha, beta):
        if depth == 0:
            return [self.calculateScoreRate(boardMatrix, not is_max), None, None]
        
        allPossibleMoves = self.generateMoves(boardMatrix)
        
        if len(allPossibleMoves) == 0:
            return [self.calculateScoreRate(boardMatrix, not is_max), None, None]
        
        bestMove = [None, None, None]
        if is_max:
            bestMove[0] = -1.0
            # Iterate for all possible moves that can be made.
            for move in allPossibleMoves:
                # Play the move to that temporary board without drawing anything
                tmpBoardMatrix = self.addStoneNoGUI(boardMatrix, move[1], move[0], False)
                
                # Call the minimax function for the next depth, to look for a minimum score.
                tempMove = self.minimax_AB(depth-1, tmpBoardMatrix, not is_max, alpha, beta)
                
                # Updating alpha
                if tempMove[0] > alpha:
                    alpha = tempMove[0]
    
                # Pruning with beta
                if alpha >= beta:
                    return tempMove
    
                if tempMove[0] > bestMove[0]:
                    bestMove = tempMove
                    bestMove[1] = move[0]
                    bestMove[2] = move[1]
    
        else:
            bestMove[0] = 100000000.0
            bestMove[1] = allPossibleMoves[0][0]
            bestMove[2] = allPossibleMoves[0][1]
            for move in allPossibleMoves:
                tmpBoardMatrix = self.addStoneNoGUI(boardMatrix, move[1], move[0], True)
                
                
                tempMove = self.minimax_AB(depth-1, tmpBoardMatrix, not is_max, alpha, beta)
                
                # Updating beta
                if tempMove[0] < beta:
                    beta = tempMove[0]
    
                # Pruning with alpha
                if beta <= alpha:
                    return tempMove
    
                if tempMove[0] < bestMove[0]:
                    bestMove = tempMove
                    bestMove[1] = move[0]
                    bestMove[2] = move[1]
        return bestMove
    
    def find_next_move_forAI(self,boardMatrix, depth):
        # for i in range(SIZE):
        #     print(boardMatrix[i])
        global winScore
        start_time = time.time()
        # print('AI start thinking...')
        
        move = []
    
        # Check if any available move can finish the game
        bestMove = self.searchWinningMove(boardMatrix)
        
        if bestMove is not None:
            move.append(bestMove[0])
            move.append(bestMove[1])
        else:
            # If there is no such move, search the minimax tree with suggested depth.
            bestMove = self.minimax_AB(depth, boardMatrix, True, -1.0, winScore)
            if bestMove[1] == None:
                move = None
            else:
                move.append(bestMove[1])
                move.append(bestMove[2])
    
        # print('AI finish thinking')
        print("--- %s seconds ---" % (time.time() - start_time))
        
        return move   
    
    def initialize(self):
        global canvas,CELL_SIZE, canvasWidth, canvasHeight,tkinter,MINIMAX_DEPTH,winScore
        winScore = 100000000
        MINIMAX_DEPTH = 3
        
        tkinter = Tk()
        tkinter.title("Caro")
        
        CELL_SIZE = 35
        canvasWidth = CELL_SIZE * self.getBoard().getWidth() + 10
        canvasHeight = CELL_SIZE * self.getBoard().getHeight() + 10
        
        canvas = Canvas(tkinter, width= canvasWidth, height= canvasHeight,background="white")
        
        canvas.pack()
        
        self.drawBoard(canvas)
        tkinter.bind("<Button-1>", lambda event:    self.mousePressed(event))
        tkinter.mainloop()

if __name__ == '__main__':
    game = Game(20, 20, 1, 5)
    game.initialize()   
    
    