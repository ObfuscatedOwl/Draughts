white = (250, 241, 220)
black = (31, 22, 0)
tileWhite = (217, 199, 154)
tileBlack = (115, 82, 39)
blue = (9, 212, 227)
red = (232, 37, 79)


def renderBoard (screen, game, width, height, Rect, posSelected, selectedPos, possibleMoves):
    

    squareSize = (int(width / 8), int(height / 8))
    
    x = 0
    
    for i in range(0, width, squareSize[0]): #for each position in the width of the board
        y = 0
        for j in range(0, height, squareSize[1]): #for each position in the height of the board
            
            theSquare = Rect((i,j), squareSize) #the current square being drawn

            if (posSelected
                    and (selectedPos == (x, y) or (x,y) in [move.pos for move in possibleMoves])): 
                    #and the current rectange is the selected pos or a possible move
                screen.draw.filled_rect(theSquare, (89, 217, 30)) #colour it this green

            
            elif (x + y) % 2 == 1: #if it needs to be white
                screen.draw.filled_rect(theSquare, tileWhite)
                
            else: #else it needs to be black
                screen.draw.filled_rect(theSquare, tileBlack)

            if game.length >= 1 and not posSelected:
                lastMoveDict = game.movesPlayed[-1]

                if (x, y) in (lastMoveDict['startPos'], lastMoveDict['endPos']):
                    screen.draw.filled_rect(theSquare, blue)

                elif (x, y) in lastMoveDict['captures']:
                    screen.draw.filled_rect(theSquare, red)



            #drawing the pieces
            currentTile = game.getTile((x,y))
            
            
            circlePos = (i + squareSize[0]/2, j + squareSize[1] / 2) 
            circleR = int(squareSize[0] / 2) - 2 #if we need to draw a circle, what its pos and radius are
            
            if currentTile['value'] == 'B':
                screen.draw.filled_circle(circlePos, circleR, black) #draw the counter
            if currentTile['value'] == 'W':
                screen.draw.filled_circle(circlePos, circleR, white)
            if currentTile['king']:
                screen.draw.filled_circle(circlePos, 10, (227, 220, 0))
            
            
            
            y += 1
            if y > 7:
                break
        x += 1 #keeping track of the position on the board
        if x > 7:
            break #avoiding index errors