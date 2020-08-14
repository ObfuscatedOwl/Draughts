import pgzrun
from boardTile import Game
from move import tryMove
from calculusTraining import alphaBeta, getMinMaxMove, getChildren
from renderBoard import renderBoard
from network import Network
import os
import random



WIDTH = 600
HEIGHT = 600

square = (int(WIDTH / 8), int(HEIGHT / 8))


white = (250, 241, 220)
black = (31, 22, 0)
tileWhite = (217, 199, 154)
tileBlack = (115, 82, 39)


posSelected = False
selectedPos = 0,0
possibleMoves = []

heuristic = False

if not heuristic:
    network = Network([144, 20, 20, 1], path = os.getcwd())


def playAiMove(game):
    if heuristic:
        return getMinMaxMove(game, 2)
    else:
        gameValues = []
        for possibleGame in getChildren(game):
            gameValues.append({'game' : possibleGame, 'value' : network.evalGame(game, game.playerToMove)})

        valueLambda = lambda x : x['value']
        random.shuffle(gameValues)

        return max(gameValues, key = valueLambda)['game']




def on_mouse_down(pos, button):

    global theGame, tryMove, posSelected, selectedPos, possibleMoves
    
    if button == mouse.LEFT:
        squarePos = int(pos[0] / square[0]), int(pos[1] / square[0]) #which square this mouse click is over
         
        #print("Mouse button", button, "clicked at square", squarePos)
        
        if posSelected: #if a position is selected
            for move in possibleMoves: #for each possible move
                if move.pos == squarePos: #if the click is on the possible move
                
                    theGame = move.game #set the game state to the result of the possible move
                    
                    
                    posSelected = False
                    possibleMoves = [] 

                    theGame = playAiMove(theGame) #play the ai's response move
                    
                    return #end here
        
        
        if not selectedPos == squarePos and theGame.getTile(squarePos)['value'] == theGame.playerToMove: #if the player has clicked on one of their own tiles
            posSelected = True
            selectedPos = squarePos #a pos has been selected
            
            possibleMoves = tryMove(squarePos, theGame)#, theGame.playerToMove) #set possible moves
            
            for move in possibleMoves:
                pass#print(move.game)
            
                
                #possibleMove =  #generate a possible move
                
                

def draw ():
    
    renderBoard(screen, theGame, WIDTH, HEIGHT, Rect, posSelected, selectedPos, possibleMoves)
  


theGame = Game()

theGame = playAiMove(theGame)

pgzrun.go()