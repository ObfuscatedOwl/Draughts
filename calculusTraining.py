from network import Network
from boardTile import Game
import math
from move import tryMove
import random
#import matplotlib.pyplot as plt
import numpy as np
import cProfile

#so what this script needs to do
#so i need to begin training the ai with heuristics
#no, first i need to create it and implement the inputs to the ai

#i should use a slot based system for the inputs (controlled kings [12], controlled men[12], enemy kings[12], enemy men[12])
#this means that there will be 48 input slots in total
#in each slot, there will be three neurons, whether the piece is present, a normalised x coordinate (x / 7), and a normalised y coordinate (y / 7)

network = Network([48 * 3, 20, 20, 1])
inputs = network.gameToInput(Game(), 'W')
#print(inputs)


#ok inputs are done
#now........
#heuristic evaluation of the chance of winning
#i want this to be a probablility based thing
#so first check if the board is in a win or loss state
#and if so set it to 1. or 0. respectively
#otherwise do some sort of evaluation to get the chance
#if there's the same number of kings and men on each side
#the value should be 0.5
#it should tend to 1. or 0. if either side has a significant number more pieces
#lol let's do this with the sigmoid function i'm not feeling very creative
#ok
#add up all of the values of the pieces on each side, men are 1, kings are 2, and enemies are negative
#then put it through the sigmoid to get the desired output
#cool
#then use alpha-beta pruning to determine what the evaluation should be
#use tree of depth... 3 or 4 idk
#actually i can probably get away with higher for drafts
#i should test


#ok!
#the heuristics with alphabeta is DONE!
#now
#training against the minmax
#then training against itself minmaxed


def getChildren(game):
    children = []
    for i in range(8):
        for j in range(8):
            if game.getTile((i, j))['value'] == game.playerToMove:
                returnedGames = tryMove((i, j), game)
                for returnedGame in returnedGames:
                    children.append(returnedGame.game)
    
    return children



def alphaBeta(game, depth, player, alpha = -math.inf, beta = math.inf, isMaximisingPlayer = True):
    if depth == 0 or game.getWinner():
        return heuristicEval(game, player)
    
    if game.playerToMove == player:
        value = -math.inf
        for childGame in getChildren(game):
            value = max(value, alphaBeta(childGame, depth - 1, player, alpha = alpha, beta = beta, isMaximisingPlayer = False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break #beta cutoff
        return value
    else:
        value = math.inf
        for childGame in getChildren(game):
            value = min(value, alphaBeta(childGame, depth - 1, player, alpha = alpha, beta = beta, isMaximisingPlayer = True))
            beta = min(beta, value)
            if beta <= alpha:
                break #alpha cutoff
        return value



def sumValues(game):
    #counts all of the values of the different pieces on the board
    #kings have value 2, men 1
    #returns a dictionary of the values of white, black
    sums = {'W' : 0, 'B' : 0}
    for i in range(8):
        for j in range(8):
            tile = game.getTile((i, j))
            if tile['value'] in ('W', 'B'):
                if not tile['king']:
                    sums[tile['value']] += 1

                elif tile['king']:
                    sums[tile['value']] += 2
    
    return sums



def sigmoid(x):
    return 1 / (1 + (math.e ** -x))



def heuristicEval(game, perspective):
    #a heuristic evaluation of game
    #perspective is the perspective of the ai,
    #i.e. if white has won and perspective == 'W'
    #the output will be 1.
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
    # plt.ion()
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # line1, = ax.plot([0], [0], 'r-')

    costData = [[], []]
    xPoint = 0

    for i in range(1):
        game = Game()
        #loops through games
        while game.length < maxGameLength:
            #print(game)
            possibleGames = getChildren(game)

            if len(possibleGames) == 0:
                break

            netOutputs = []
            nabla_bL = []
            nabla_wL = []
            costL = []

            for possibleGame in possibleGames:
                minmaxEval = alphaBeta(possibleGame, 2, game.playerToMove)
                netInput = network.gameToInput(game, game.playerToMove)
                nabla_b, nabla_w, output = network.backprop(netInput, minmaxEval)
                netOutputs.append({'game' : possibleGame, 'netValue' : output})
                nabla_bL.append(nabla_b)
                nabla_wL.append(nabla_w)
                costL.append(((minmaxEval - output[0]) ** 2)[0])

            network.updateWB(nabla_bL, nabla_wL, learningRate)
            averageCost = sum(costL) / len(costL)
            costData[0].append(xPoint)
            xPoint += 1
            costData[1].append(averageCost)
            print(costData[1][-1])
            #updateLine(fig, line1, costData[0], costData[1])

            valueLambda = lambda x : x['netValue']
            random.shuffle(netOutputs)
            game = max(netOutputs, key = valueLambda)['game']

             

if __name__ == '__main__':
    cProfile.run('train(Network([144, 20, 20, 1]), 100, 0.1)')
    
