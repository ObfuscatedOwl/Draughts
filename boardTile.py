import copy

def createTile(value):

    directions = ()
    
    if value == 'B':
        directions = ((-1, 1), (1, 1)) #directions a piece can move at the start of the game
    if value == 'W':
        directions = ((-1, -1), (1, -1))


    return {'value' : value, 'directions' : directions, 'king' : False}



class Game:
    def __init__(self):
        self.board = self.generateBoard() #generate the board
        
        self.playerToMove = 'W'
        
        self.scores = {'W' : 0, 'B' : 0} #scores of each player (used to find when a player has got all of the other's pieces)
        self.length = 0

        self.movesPlayed = []



    def generateBoard(self): #generates a list of lists with tile objects in the setup of a game
        board = []
        
        for i in range(8): #for the width of the board
            column = [] 
            for j in range(8): #for the height of the board
                if (i + j) % 2 == 0: #if on the first of every 2 tiles
                    if j <= 2: #if at the top of the board
                        tileColour = 'B' 
                        
                    elif j >= 5: #if at the bottom of the board
                        tileColour = 'W'
                        
                    else: #else no counter on the tile
                        tileColour = '-'
                
                
                    column.append(createTile(tileColour)) #initialise and append the current tile
                    
                else:
                    column.append(createTile(' ')) #initialise and append a blank tile
                    
            board.append(column) #add the column to the board
        
        return board
    
    
    
    def __str__(self): #string representation of the board
        output = []
        
        for i in range(8):
            for j in range(8):
                output.append((self.board[j][i])['value'] + ' ') 
            output.append('\n')
            
        return ''.join(output)
        
        
        
    def getTile(self, pos): #get the value of a tile on the board
        return self.board[pos[0]][pos[1]]
        
        
        
    def setTile(self, pos, value): #set the value of a tile on the board
        if type(value) == dict: #if the type of the value to set to is a Tile
            self.board[pos[0]][pos[1]] = value
        
        if type(value) == str: #if the type of the value is a string
            self.board[pos[0]][pos[1]] = createTile(value)
            


    def copy(self):
        theCopy = Game()

        theCopy.board = [[tile.copy() for tile in column] for column in self.board]

        theCopy.playerToMove = self.playerToMove
        theCopy.scores = self.scores.copy()
        theCopy.length = self.length

        theCopy.movesPlayed = self.movesPlayed.copy()
        for movePlayed, i in zip(self.movesPlayed, range(len(self.movesPlayed))):
            theCopy.movesPlayed[i] = movePlayed.copy()
            theCopy.movesPlayed[i]['captures'] = movePlayed['captures'].copy()
            

        return theCopy
    


    def getWinner(self):
        #returns False if there is no winner and the value of the winner if there is
        for scoreTuple in self.scores.items():
            if scoreTuple[1] == 12: #if this player has twelve captures
                return scoreTuple[0] #they have won
        
        return False #neither player has won

        
    