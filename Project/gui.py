import wx
import os
import wx.lib.newevent

#create an AI event which will trigger the move for AI
AIEvent, AI_EVENT = wx.lib.newevent.NewEvent()

class GameWindow(wx.Frame):

    def __init__(self, parent, title,board,minmax):
        """constructor setup the variables"""
        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        self.turn=0
        self.row = board.row
        self.col = board.col
        self.board = board
        self.minmax = minmax
        size = (800,1000)
        wx.Frame.__init__(self, parent, title=title, size=size)
        
        self.CreateStatusBar() # A Statusbar in the bottom of the window
        #bind the AI event with the AI thinking method
        self.Bind(AI_EVENT, self.makeAIMove)

        #setup the board layout
        self.setup()

        #ask the user if he wants to go first or the computer
        if self.YesNo("Do You want to go first?", "First Move") is False:
            self.turn = 1
            self.makeAIMove(None)

        
    #dialog to ask for first move
    def YesNo(parent, question, caption = ''):
        dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()
        return result
    #dialog to decalre the result
    def Info(parent, message, caption = ''):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
   
    #handler to make the human player to move
    def makeHumanMove(self,e):
        if self.turn != 0:
            return
        self.turn = 1
        widget = e.GetEventObject()
        i = int( widget.GetName() )

        row = i / self.col
        col = i % self.col
        self.board.updateBoard(row,col,'O')

        self.grid[i].Enable(False)
        self.grid[i].SetLabel("O")
        self.grid[i].SetBackgroundColour((0,0,0))
        self.sizer2.Layout()
        self.sizer.Layout()
        #see if player has won
        if self.board.checkVictoryforSymbol('O'):
            self.Info("You Won ", "This is embarrassing")
            return

        if len(self.minmax.actionGenerator(self.board)) == 0:
            self.Info("You are a worthy competitor!","Its a Draw")
            return

        #trigger the event for AI to start thinking
        evt = AIEvent()
        wx.PostEvent(self,evt)
        

    #handler to make the AI move
    def makeAIMove(self,e):
        move = self.minmax.getNextMove(self.board)
        x = move[0]
        y = move[1]
        self.board.updateBoard(x,y,self.minmax.symbolAI)
        i = x*self.col + y
        self.grid[i].Enable(False)
        self.grid[i].SetLabel("X")
        self.grid[i].SetBackgroundColour((255,0,0))
        self.sizer2.Layout()
        self.sizer.Layout()
        
        if self.board.checkVictoryforSymbol('X'):
            self.Info("You Lost", "You Lost")
            return
        if len(self.minmax.actionGenerator(self.board)) == 0:
            self.Info("You are a worthy competitor","Its a Draw")
            return


        self.turn=0

    #utility setup method used by the constructor
    def setup(self):
        self.sizer2 = wx.GridSizer(self.row,self.col)
        self.grid = []
        for i in range(0, 20):
                self.grid.append(wx.Button(self, -1, "-",size =(100,100),name = str(i)) )
                self.sizer2.Add(self.grid[i],1,wx.EXPAND)
                self.Bind(wx.EVT_BUTTON, self.makeHumanMove,self.grid[i])

        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.sizer2, 1, wx.EXPAND)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show()
