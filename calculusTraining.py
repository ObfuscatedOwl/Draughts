from network import Network
from boardTile import Game
import math
from move import tryMove
import random
#import matplotlib.pyplot as plt
import numpy as np
import cProfile
import os



def getChildren(game):
    """Returns all the possible states reached one move from game."""
    children = []
    for i in range(8):
        for j in range(8):#for each tile on the board
            if game.getTile((i, j))['value'] == game.playerToMove: #if the tile's value is the player to move

                returnedGames = tryMove((i, j), game) #find all the possible games reached from this point

                for returnedGame in returnedGames:
                    children.append(returnedGame.game)
    
    return children



def alphaBeta(game, depth, player, alpha = -math.inf, beta = math.inf):
    """Returns the minmax value of a game state, using alpha-beta pruning and looking depth nodes ahead.

    player (either 'W' or 'B') - the player that is maximised.
    """
    if depth == 0 or game.getWinner():
        return heuristicEval(game, player)
    
    if game.playerToMove == player:
        value = -math.inf
        for childGame in getChildren(game):
            value = max(value, alphaBeta(childGame, depth - 1, player, alpha = alpha, beta = beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break #beta cutoff
        return value

    else:
        value = math.inf
        for childGame in getChildren(game):
            value = min(value, alphaBeta(childGame, depth - 1, player, alpha = alpha, beta = beta))
            beta = min(beta, value)
            if beta <= alpha:
                break #alpha cutoff
        return value



def sumValues(game):
    """counts all of the values of the different pieces on game.board

    kings have value 2, men 1
    returns a dictionary of the values of white, black"""
    sums = {'W' : 0, 'B' : 0}

    for i in range(8):
        for j in range(8): #for each tile on the board
            tile = game.getTile((i, j))
            if tile['value'] in ('W', 'B'): #if the tile is not empty
                if not tile['king']:
                    sums[tile['value']] += 1

                elif tile['king']:
                    sums[tile['value']] += 2
    
    return sums



def sigmoid(x):
    return 1 / (1 + (math.e ** -x))



def heuristicEval(game, perspective):
    """A heuristic evaluation of game based on the number of different pieces.

    Perspective is the player with the perspective of this evaluation,
    i.e. if white has won and perspective == 'W'
    the output will be 1."""
    if (winner := game.getWinner()):
        if winner == perspective:
            return 1.
        else:
            return 0.

    else:
        sums = sumValues(game)
        oppositePlayer = {'W' : 'B', 'B' : 'W'}[perspective]
        sumValue = sums[perspective] - sums[oppositePlayer]
        return sigmoid(sumValue)



def getMinMaxMove(game, depth):
    """Returns the move chosen by the alphabeta function at a certain depth."""

    possibleGames = [{'game' : possibleGame, 'value' : 0} for possibleGame in getChildren(game)]
    for possibleGame in possibleGames:
        possibleGame['value'] = alphaBeta(possibleGame['game'], depth, game.playerToMove)
    
    valueLambda = lambda x : x['value']
    random.shuffle(possibleGames)

    return max(possibleGames, key = valueLambda)['game']



def updateLine(fig, line, xData, yData):
    line.set_xdata(xData)
    line.set_ydata(yData)
    fig.canvas.draw()
    fig.canvas.flush_events()



def train(network, maxGameLength, learningRate, heuristic = True):
    """Trains a network."""
    # plt.ion()
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # line1, = ax.plot([0], [0], 'r-')

    costData = [[], []]
    xPoint = 0

    while True:
        game = Game()
        #loops through games
        while game.length < maxGameLength:
            possibleGames = getChildren(game)

            if len(possibleGames) == 0:
                print("Game finished, no possible moves.")
                print(game)
                print('---------------------------------')
                break

            netOutputs = []
            nabla_bL = []
            nabla_wL = []
            costL = []

            for possibleGame in possibleGames:
                minmaxEval = max(0, alphaBeta(possibleGame, 2, game.playerToMove)) #get the heuristic minmax value

                netInput = network.gameToInput(game, game.playerToMove) #generate the input to the network
                nabla_b, nabla_w, output = network.backprop(netInput, minmaxEval) #get the derivitives of C with respect to w and b

                netOutputs.append({'game' : possibleGame, 'netValue' : output}) #record the output of the net

                nabla_bL.append(nabla_b)
                nabla_wL.append(nabla_w)
                cost = ((minmaxEval - output[0]) ** 2)[0]
                costL.append(cost)
                if cost == np.inf or cost == np.nan:
                    print(f"minmaxEval : {minmaxEval}")
                    print(f"output : {output[0]}")


            network.updateWB(nabla_bL, nabla_wL, learningRate) #update the weights and biases of the network

            averageCost = sum(costL) / len(costL)
            costData[0].append(xPoint)
            xPoint += 1
            costData[1].append(averageCost)
            print(averageCost)
            if averageCost == np.inf or averageCost == np.nan:
                print('Inf or Nan value encountered.')
                print(f'costL = {costL}')

            #updateLine(fig, line1, costData[0], costData[1])

            valueLambda = lambda x : x['netValue']
            random.shuffle(netOutputs)
            game = max(netOutputs, key = valueLambda)['game'] #set the game the net chooses as the next one


        network.save(os.getcwd())

             

if __name__ == '__main__':
    network = False
    while not network:
        userInput = input('Load saved network? (y/n): ')

        if userInput == 'y':
            network = Network([144, 20, 20, 1], path = os.getcwd())

        elif userInput == 'n':
            network = Network([144, 20, 20, 1])

        else:
            print('Invalid input.')
        
    #cProfile.run('train(Network([144, 20, 20, 1]), 100, 0.1)')
    train(network, 100, 0.1)
    
