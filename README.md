# Draughts
A project implementing the game draughts and a neural network play it.

PvP.py allows you to play against another player
VsAi.py (currently) allows you to play against a minmax player.

calculusTraining.py is the program for training the network.
boardTile.py contains the definition of the Game.
move.py contains a function tryMove that takes a Game and a position and returns the possible games that can be reached by moving the stone at that position.
network.py contains the definition of the Network class.
renderboard.py contains a function that draws the board to a pygame zero screen.
