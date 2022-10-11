import turtle
from random import randint as rand

players = 1

hardcodedchecks = [ # couldn't be bothered to make this efficient-er so I just stole the checks from my old tic tac toe and remade them more efficiently.
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 6, 6, 7],
    [1, 2, 3, 6, 4, 8, 2, 4, 7, 5, 8, 4, 6, 4, 5, 6, 4, 7, 8, 6, 8, 7, 8, 8],
    [2, 1, 6, 3, 8, 5, 0, 7, 4, 8, 5, 6, 4, 5, 4, 0, 3, 1, 0, 2, 2, 8, 7, 6]
]
board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
availableboard = [True, True, True, True, True, True, True, True, True]

screen = turtle.Screen()
turn = 2

class TicTacToeBoard:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(600, 600)
        self.screen.bgpic("tttboard.gif")
        self.screen.addshape("x.gif")
        self.screen.addshape("o.gif")
        self.screen.addshape("empty.gif")
        self.screen.tracer(0)
    
    def updateScreen(self): self.screen.update()
    def die(self, x = None, y = None): self.screen.bye()

    def end(self, team):
        global boardobj, tiles, endgame
        if team - 1 and team: self.screen.bgpic("xwin.gif")
        elif team: self.screen.bgpic("owin.gif")
        else: self.screen.bgpic("tiewin.gif")
        for i in tiles: i.turtle.hideturtle()
        self.screen.update()
        self.screen.onclick(self.die)

class Tile:
    def __init__(self, column, row):
        self.row = row
        self.column = column
        self.locations = [-200, 0, 200]
        self.turtle = turtle.Turtle()
        self.turtle.pu()
        self.turtle.lt(90)
        self.turtle.shape("empty.gif")
        self.turtle.goto(self.locations[column], self.locations[row])
        self.tiled = False
    
    def checkForEnd(self, available, board, team):
        for i in range(3):
            if team == board[3 * i] == board[3 * i + 1] == board[3 * i + 2]: return 1 # Win vertically
            if team == board[i] == board[i + 3] == board[i + 6]: return 1 # Win horizontally
        if (team == board[0] == board[4] == board[8]) or (team == board[2] == board[4] == board[6]): return 1 # Win diagnally
        if available.count(True) == 0: return 2 # Tie
        return 0 # None

    def setShape(self, shape, availableboard, boardobj, board):
        if not self.tiled:
            if shape - 1: self.turtle.shape("x.gif")
            else: self.turtle.shape("o.gif")
            self.tiled = True
            availableboard[self.column + self.row * 3] = False
            board[self.column + self.row * 3] = shape
            boardobj.updateScreen()
            return True
        return False

boardobj = TicTacToeBoard()
tiles = []
for row in range(3):
    for column in range(3):
        tiles.append(Tile(column, row))

def checkForAIMove(board, availableboard, team):
    global hardcodedchecks
    
    for i in range(len(hardcodedchecks[0])):
        if board[hardcodedchecks[0][i]] == board[hardcodedchecks[1][i]] == team and availableboard[hardcodedchecks[2][i]]: return hardcodedchecks[2][i]
    return -1
def clickTrigger(x, y):
    global turn, players
    if x <= -96: xcor = 0
    elif x >= 96: xcor = 2
    else: xcor = 1

    if y <= -97: ycor = 0
    elif y >= 87: ycor = 2
    else: ycor = 1
    x = tiles[xcor + ycor * 3].setShape(turn, availableboard, boardobj, board)
    if x:
        wincondition = tiles[xcor + ycor * 3].checkForEnd(availableboard, board, turn)
        if wincondition == 2: boardobj.end(0)
        elif wincondition: boardobj.end(turn)

        if turn - 1: turn -= 1
        else: turn += 1

    if not x: return False
    if wincondition: return False
    if players == 1:
        computerTile = checkForAIMove(board, availableboard, 1)
        if computerTile == -1:
            computerTile = checkForAIMove(board, availableboard, 2)
        if computerTile == -1:
            computerTile = rand(0,8)
        
        while not tiles[computerTile].setShape(turn, availableboard, boardobj, board):
            computerTile = rand(0,8)
        
        wincondition = tiles[computerTile].checkForEnd(availableboard, board, turn)
        if wincondition == 2: boardobj.end(0)
        elif wincondition: boardobj.end(turn)

        if turn - 1: turn -= 1
        else: turn += 1

screen.onclick(clickTrigger)
screen.update()
screen.mainloop()
