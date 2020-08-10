import copy

class ReturnedMove:
    def __init__(self, pos, game):
        self.pos = pos
        self.game = game



def inside(pos): #says if a point is inside the board
    return (pos[0] < 8 and pos[0] > -1 and pos[1] < 8 and pos[1] > -1)
    

def getLeaps(directions, pos, game, prevTrialGame, colour): #gets any possible leap moves that can be played
    possibleLeaps = []
    
    for direction in directions: #for each direction of the tile
        trialGame = prevTrialGame.copy() #create a new trial game to try the move
        movePos = (pos[0] + direction[0], pos[1] + direction[1])
        leapPos = (pos[0] + direction[0] * 2, pos[1] + direction[1] * 2)
        
        
        if colour == 'B':
            oppositeColour = 'W'
        if colour == 'W':
            oppositeColour = 'B'
        
        
        if inside(leapPos) and  trialGame.getTile(movePos)['value'] == oppositeColour and trialGame.getTile(leapPos)['value'] == '-': #if the leap pos is within the board if the leap pos is empty
        
            #look to see if a double jump is possible
        
            trialGame.setTile(movePos, '-')
            trialGame.setTile(pos, '-')
            trialGame.setTile(leapPos, prevTrialGame.getTile(pos).copy()) #play the leap move on the trial game
            trialGame.scores[colour] += 1

            trialGame.movesPlayed[-1]['endPos'] = leapPos
            trialGame.movesPlayed[-1]['captures'].append(movePos)

            possibleLeaps.append( ReturnedMove(leapPos, trialGame)) #add the trial game to the list of possible moves
            
            
            for i in getLeaps(directions, leapPos, game, trialGame, colour):
                possibleLeaps.append(i) #recurse to try if another leap is possible
                    
                    
    return possibleLeaps



def tryMove(startPos, game):

    possibleMoves = []
    
    tileMoving = game.getTile(startPos)
    directions = tileMoving['directions'] #the directions the tile can go 
    colour = tileMoving['value'] #the colour of the tile
        
    for direction in directions: #for each diagonal direction
        trialGame = game.copy()

        movePos = startPos[0] + direction[0], startPos[1] + direction[1] #resulting pos for a normal move
        
        trialGame.movesPlayed.append({'startPos' : startPos, 'endPos' : movePos, 'captures' : []}) 
        #add a dictionary to show how this game was affected by the move
    
        if inside(movePos): #if the move position is inside the board
            
            if trialGame.getTile(movePos)['value'] == '-': #if the move position is empty
                trialGame.setTile(startPos, '-')
                trialGame.setTile(movePos, game.getTile(startPos).copy()) 
                possibleMoves.append( ReturnedMove(movePos, trialGame) )      #play the move
                
            elif trialGame.getTile(movePos)['value'] == colour: #if the player's colour is in the way
                pass#return ReturnedMove(False, (0,0), trialGame) #it is not allowed
                
            else:
                possibleLeaps = getLeaps(directions, startPos, game, trialGame, colour) #get possible leap moves
                for i in possibleLeaps: #for every possible leap move 
                    possibleMoves.append(i) #add it to the possible moves
            
        else:
            pass#the player is not allowed to play if the move pos is not within the board
            
            
    for move in possibleMoves:
        endRows = {'W' : 0, 'B' : 7}
        endRow = endRows[colour]
        
        #print(move.game.getTile(move.pos) is game.getTile(move.pos)) 
        
        if move.pos[1] == endRow:
            newKing = move.game.getTile(move.pos)
            newKing['directions'] = ((-1, 1), (1, 1), (-1, -1), (1, -1)) 
            newKing['king'] = True
            

        move.game.length += 1
        
        if move.game.playerToMove == 'W':
            move.game.playerToMove = 'B'
        elif move.game.playerToMove == 'B':
            move.game.playerToMove = 'W' #change whose turn it is to move
        
       
    return possibleMoves