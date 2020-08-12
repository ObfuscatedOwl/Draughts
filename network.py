import numpy as np
import math


def sigmoid(x):
    return 1 / (1 + (math.e ** -x))

def sigmoid_prime(x):
    return sigmoid(x) * (1 - sigmoid(x))


class Network:
    def __init__(self, layerSizes, path = False):

        if not path:
            self.weights = [np.random.standard_normal(s) / math.sqrt(s[1]) for s in zip(layerSizes[1:], layerSizes[:-1])]
            self.biases = [np.zeros([s, 1]) for s in layerSizes[1:]]
            self.numLayers = len(layerSizes)
            self.layerSizes = layerSizes

        elif path:
            self.weights = np.load(path + '\\weights.npy', allow_pickle= True)
            self.biases = np.load(path + '\\biases.npy', allow_pickle= True)
            self.layerSizes = list(np.load(path + '\\layerSizes.npy', allow_pickle= True))
            self.numLayers = len(self.layerSizes)


    def cost_derivitive(self, output_activations, y):
        return (output_activations - y)
        

    def getOutput(self, inputV):
        a = inputV
        for i in range(0, self.numLayers - 1):
            z = np.dot(self.weights[i], a) + self.biases[i]
            a = sigmoid(z)

        return a


    def backprop(self, x, y): #x is the input, y is the output the network should give
        
        nabla_b = [np.zeros(b.shape) for b in self.biases] #defining the partial derivitives of the weights and biases
        nabla_w = [np.zeros(w.shape) for w in self.biases] #these will be the output of the function

        #feedforward
        zs = []
        activation = x
        activations = [x] 

        for w, b in zip(self.weights, self.biases):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)

        #backpropogate errors

        delta = self.cost_derivitive(activations[-1], y) * \
            sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())

        for l in range(2, self.numLayers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())

        return (nabla_b, nabla_w, activation)



    def gameToInput(self, game, player):
        friendlyKings = [] #lists of positions of these pieces
        friendlyMen = []
        enemyKings = []
        enemyMen = []

        enemyPlayer = {'B': 'W', 'W': 'B'}[player] #value of the enemy player string

        if player == 'W':
            transformMatrix = np.identity(2)
        elif player == 'B':
            transformMatrix = np.identity(2).transpose() #transformation rotates the board by 180 degrees, keeps the perspective the same

        for i in range(8):
            for j in range(8):
                pos = (i, j)
                pos = np.dot(transformMatrix, pos) #means the ai's perspective doesn't change from w to b
                tile = game.getTile((int(pos[0]), int(pos[1])))

                if tile['value'] == player:
                    if tile['king']:
                        friendlyKings.append(pos)
                    else:
                        friendlyMen.append(pos)

                if tile['value'] == enemyPlayer:
                    if tile['king']:
                        enemyKings.append(pos)
                    else:
                        enemyMen.append(pos)
        
        
        inputs = np.zeros((48 * 3, 1)) #3 nodes for each of 48 slots

        for sectionI, l in zip(range(4), (friendlyKings, friendlyMen, enemyKings, enemyMen)):
            for i, pos in zip(range(12), l):
                inputs[sectionI * 3 * 12 + i * 3 + 0] = 1 #the piece is present
                inputs[sectionI * 3 * 12 + i * 3 + 1] = pos[0] / 7 #normalised x position of piece
                inputs[sectionI * 3 * 12 + i * 3 + 2] = pos[1] / 7 #normalised y position of piece

        return inputs



    def updateWB(self, nabla_bL, nabla_wL, eta):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        
        for delta_nabla_b, delta_nabla_w in zip(nabla_bL, nabla_wL):
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]

        self.weights = [w-(eta/len(nabla_bL))*nw 
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(nabla_bL))*nb 
                       for b, nb in zip(self.biases, nabla_b)]

    

    def save(self, path):
        np.save(path + '\\weights.npy', self.weights)
        np.save(path + '\\biases.npy', self.biases)
        np.save(path + '\\layerSizes.npy', self.layerSizes)

                    
                    
if __name__ == '__main__':
    network = Network([2, 30000, 2])
    print(network.getOutput([[0.8], [0.3]]))

    from boardTile import Game

    print(network.gameToInput(Game(), 'W'))
    