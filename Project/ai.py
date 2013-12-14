import random
import copy
import time
import sys
import wx
from gui import GameWindow

"""This class represents the Board"""
"""the four 45 and 135 deg diagonals in a 4x5 board are represented below"""
class Board:
    diagonals =		[ [(0,0),(1,1),(2,2),(3,3)],
    				 [(0,1),(1,2),(2,3),(3,4)],
    				 [(0,4),(1,3),(2,2),(3,1)],
    				 [(0,3),(1,2),(2,1),(3,0)] ]

    """constructor initializes the grid and parameters
    row - no of rows
    col - no of columns
    victoryNo - the length of consecutive symbols needed for victory
    turns - the amount of moves made on the board"""
    def __init__(self,row,col,victoryNo):
    	self.grid = []
        #initialize board
        self.row = row
        self.col = col
        self.victoryNo = victoryNo
        self.turns = 0

        for i in range(0,row):
            temp = []
            for j in range(0,col):
                temp.append(0)
            self.grid.append(temp)


    def updateBoard(self,row,col,symbol):
    	"""update the board with a new move"""
    	self.grid[row][col] = symbol
    	self.turns += 1
    	return self


    def checkVictoryforSymbol(self,symbol):
    	"""checks if player of a particular symbol has won"""
    	#all the diagonals which are to be checked
    	diagonals = Board.diagonals

    	#check for rows
    	for i in range (0 , self.row):
    			if self.evaluate(self.grid[i], symbol, self.victoryNo):
    				return True
    	

    	#check for columns
    	for i in range(0,self.col):
    		temp = []
    		for j in range(0,self.row):
    			temp.append( self.grid[j][i] )
    		if self.evaluate(temp,symbol,self.victoryNo):
    			return True

    	#check for diagonals
    	for diagonal in diagonals:
    		temp = []
    		for i,j in diagonal:
    			temp.append( self.grid[i][j] )
    		if self.evaluate(temp,symbol,self.victoryNo):
    			return True

    	return False


    def evaluate(self,lst, sym, victoryNo):
    	"""accepts -
    		a list of board values, can be any position, the calling method has to take care of it,
    		the symbol whose victory is to be checked
    		victory no - the no of consecutive positions which will award victory to a player"""
    	count = 0
    	for item in lst:
    		if item == sym:
    			count += 1
    		else:
    			count = 0
    		if count == victoryNo:
    			return True
    	return False

    @staticmethod
    def clone(oldboard):
    	"""clones a board"""
    	row = oldboard.row
    	col = oldboard.col
    	victoryNo = oldboard.victoryNo

    	newBoard = Board(row,col,victoryNo)

    	for i in range(0,row):
    		for j in range(0,col):
    			newBoard.grid[i][j] = oldboard.grid[i][j]
    	newBoard.turns = oldboard.turns

    	return newBoard



class Heuristic:
	@staticmethod
	def evaluate(board,minmax):
		"""evaluates a board position according to following strategy
		possible wins = no of open rows , cols or diagonals where a symbol can win. (only those rows,cols or diagonals are evaluated which have the symbol present)
		since AI plays MAX, therefore the value returned is 
		possiblewinsAI - possiblewinsHuman"""
		possibleWinsAI = Heuristic.calculatePossibleWins( board, minmax.symbolAI, minmax.symbolHuman )
		possibleWinsHuman = Heuristic.calculatePossibleWins( board, minmax.symbolHuman, minmax.symbolAI )
		
		return possibleWinsAI - possibleWinsHuman

	@staticmethod
	def calculatePossibleWins(board,symbol,enemySymbol):
		winnableRows= []
		winnableCols= []
		winnableDiags = []
		r =0
		c =0 
		d = 0
		#find num of winnable rows
		for i in range(0,board.row):
			for j in range(0,board.col):
				if board.grid[i][j] == symbol:
					if i not in winnableRows:
						r = Heuristic.evaluateRow(i,j,board,symbol,enemySymbol)
					if r is not None:
						winnableRows.append(r)

					if c not in winnableCols:
						c = Heuristic.evaluateCol(i,j,board,symbol,enemySymbol)
					if (c is not None):
						winnableCols.append(c)

					d = Heuristic.evaluateDiagonal(i,j,board,symbol,enemySymbol)
					for item in d:
						if item not in winnableDiags:
							winnableDiags.append(item)
		return len(winnableRows) + len(winnableCols) + len(winnableDiags)

	@staticmethod
	def evaluateRow(row,col,board,symbol,enemySymbol):
		count = 0

		for j in range(0,board.col):
			if count == board.victoryNo:
				return row

			if board.grid[row][j] == symbol or board.grid[row][j] == 0 :
				count += 1
			else:
				count = 0

		if count == board.victoryNo:
				return row
		return None

	@staticmethod
	def evaluateCol(row,col,board,symbol,enemySymbol):
		count = 0
		for i in range(0,board.row):
			if board.grid[i][col] == symbol or board.grid[i][col] == 0 :
				count += 1
			else:
				count = 0

			if count == board.victoryNo:
				return col

		
		return None

	@staticmethod
	def evaluateDiagonal(row,col,board,symbol,enemySymbol):
		diagonals = Board.diagonals
		d = []
		winnable = []
		count = 0
		searchkey = (row,col)
		#find which diagonal(s) contain the key	
		for diagonal in diagonals:
			for tupple in diagonal:
				if searchkey == tupple:
					d.append(diagonal)
					break

		if len(d) == 0:
			return winnable

		for diagonal in d:
			for i,j in diagonal:

				if board.grid[i][j] == symbol or board.grid[i][j] == 0:
					count += 1
				else:
					count = 0

			if count == board.victoryNo:
				winnable.append(diagonal)

		return winnable



class MinMax:
	

	positiveInf = float("inf")
	negativeInf = -float("inf")

	def __init__(self, symbolAI, symbolHuman , maxUtilValue, minUtilValue):
		"""constructor initializes the parameters
		searchDepthLimit - cut off depth for a search
		symbolAI , symbolHuman - AI and human symbols
		MAX - utility value for a win by MAX_VALUE
		MIN - utility value for a win by Min Value"""
		#default search depth limit, overwritten by the apha beta routine to a more appropriate value
		self.searchDepthLimit = 20
		self.symbolAI = symbolAI
		self.symbolHuman = symbolHuman
		self.MAX = maxUtilValue
		self.MIN = minUtilValue



	
	def actionGenerator(self, board):
		"""returns a list which contains all empty slots in the board"""
		ret = []
		for i in range(0,board.row):
			for j in range(0,board.col):
				if board.grid[i][j] == 0:
					ret.append((i,j))
		#randomize the list being returned
		if len(ret) != 0:
			random.shuffle(ret)
#		print "possible moves " + str(len(ret))
		return ret

	
	def utility(self, board):
		"""this function serves as the End condition and victory test
		returns : None if termination condition not satisfied (nobody has won and still moves are left) 
				  else it returns a a tuple (utility value, action)
				  the action value = None as there is no action to take, the calling function keeps track of the action which caused this board position"""

		#return max utility value for AI win
		if board.checkVictoryforSymbol(self.symbolAI):
			return (self.MAX, None)
		#return min utility value for human win
		if board.checkVictoryforSymbol(self.symbolHuman):
			return (self.MIN, None)

		#count no of moves left in board
		if board.turns < 20:
			#if there is a move left on the board
			return None

		#no one won and no moves left, return 0 for a tie
		return (0,None)
	
	
	def ALPHA_BETA_SEARCH(self, board):
		l = 20-board.turns
		if l >= 16:
			self.searchDepthLimit = 5
		elif l >= 14:
			self.searchDepthLimit = 6
		elif l > 12:
			self.searchDepthLimit = 7
		else:
			self.searchDepthLimit = 10

		#passing min possible util value and max possible util value as alpha and beta values instead of infinity
		return self.MAX_VALUE( Board.clone(board), self.MIN, self.MAX,1 )[1]

	
	def MAX_VALUE(self,board,alpha,beta,searchDepth):
		"""alpha beta max search with one little difference, this search returns the corresponding action along with the v value in a tuple
		return : the tuple (v, action)
		inside the for loop:
		v is used to store the utility value which will be returned later. whereas prevAction is used to store the action corresponding the v value"""
		#Check if evaluation function should kick in
		#check if the depth limit has been crossed and even number of moves have been made on the board (the heuristic is unfair if one of the players has made more moves)
		if ( searchDepth >= self.searchDepthLimit and board.turns%2 ==0 ):
			utilityValue = Heuristic.evaluate(board,self)
			return (utilityValue, None)


		#check for termination condidition
		a = self.utility(board)
		# if termination condition met then return
		#utility returns None if termination condition has not been met and there is more searching to be done
		if a is not None:
			return a
		#initialize V to negative infinity
		v = MinMax.negativeInf
		#generate all the actions
		actions = self.actionGenerator(board)
		prevAction = None
		for action in actions:
			
			#create a clone of the current board and apply the new action to it
			newBoard = Board.clone(board).updateBoard( action[0] ,action[1],self.symbolAI )
			#calculate the min value corresponding to new board
			minval = self.MIN_VALUE( newBoard, alpha, beta,searchDepth+1)[0] # accessing [0] because we are interested only in the value v from the tuple (v,action)
			#find the maximum of v and minval and also return the corresponding action
			v,prevAction = self.MAXIMUM(v, minval ,prevAction, action )
			#beta pruning happeing in this condition
			if v >= beta:
				return (v , prevAction)
			alpha = max(alpha,v)
		return (v,prevAction)


	
	def MIN_VALUE(self,board,alpha,beta,searchDepth):
		"""mirror function of the MAX_VALUE function described above"""
		if (searchDepth >= self.searchDepthLimit and board.turns%2 ==0 ):
			utilityValue = Heuristic.evaluate(board,self)
			return (utilityValue, None)

		a = self.utility(board)
		if a is not None:
			return a
		lst = []
		v = MinMax.positiveInf
		#generate all the actions
		actions = self.actionGenerator(board)
		prevAction = None
		for action in actions:
			newBoard = Board.clone(board).updateBoard( action[0] ,action[1], self.symbolHuman )
			maxvalue = self.MAX_VALUE( newBoard , alpha, beta,searchDepth+1)[0]
			v,actn = self.MINIMUM(v, maxvalue, prevAction, action )
			if v <= alpha:
				return (v , prevAction)
			beta = min(beta,v)
		return (v,prevAction)


	
	def MAXIMUM(self,v,minvalue,oldaction, newaction):
		"""returns the tuple (value, action) if the original v is maximum then original action is returned 
		else newaction with newvalue is returned"""
		if v >= minvalue:
			return (v,oldaction)
		else:
			return (minvalue,newaction)
	
	def MINIMUM(self, v,maxvalue,oldaction, newaction):
		"""mirror function of MAXIMUM described above"""
		if v <= maxvalue:
			return (v,oldaction)
		else:
			return (maxvalue,newaction)
	
	def getNextMove(self, board):
		"""wrapper function to fetch the next move from alpha beta pruning"""
		print "starting thinking now " + str(time.clock())
		move = self.ALPHA_BETA_SEARCH(board)
		print "finished now " + str(time.clock())
		return move



class Game:
	"""this class sets up the game and its objects"""
	def __init__(self):
		#initialize stuff
		self.brd = Board(4,5,4)
		self.symbolAI = 'X'
		self.symbolHuman = 'O'
		#maximum and minimum values that eval function returns is 13 and -13, so utility values for max and min are 15 and -15
		self.maxUtilValue = 15
		self.minUtilValue = -15
		minmax = MinMax(self.symbolAI,self.symbolHuman,self.maxUtilValue,self.minUtilValue)
		#initialize GUI
		app = wx.App(False)
		self.gamewindow = GameWindow(None,"4x5 tic tac toe",self.brd,minmax)
		app.MainLoop()
		


game = Game()





