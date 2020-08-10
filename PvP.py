import pgzrun
from boardTile import Game
from move import tryMove
from renderBoard import renderBoard


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



pgzrun.go()