"""
Ping pong puzzle in cpmpy.

This is a port (+ extension) of the z3 model from
From https://gist.github.com/MariaRigaki/b93f89cad49c7e7e35d94eed7abae5c3#file-ping_pong-py-L5
'''
Solution for the following problem:
3 friends (A, B and C) play ping-pong all day.
The winner always keeps playing. A plays 10 games, B 15, C 17. Who lost the 2nd game?
Problem by @eldracote https://twitter.com/eldracote/status/939614390571200514
'''

There are 420 possible solutions according to this model.
A lost the second game in all possible solutions,
in fact, A lost all the games he/she played.

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from cpmpy_hakank import *


def ping_pong():

    num_games = 21
    dnp = 0 # do not play
    loss = 1
    win = 2

    num_played = [10,15,17]

    # Keep track of the players results (2 means win, 1 means loss, 0 is DNP)
    A = intvar(dnp,win,shape=num_games,name="a")
    B = intvar(dnp,win,shape=num_games,name="b")
    C = intvar(dnp,win,shape=num_games,name="c")    

    # Keep track whether each player played or not
    playedA = boolvar(shape=num_games,name="playedA")
    playedB = boolvar(shape=num_games,name="playedB")
    playedC = boolvar(shape=num_games,name="playedC")    

    model = Model()

    for i in range(num_games):
        model += (A[i] + B[i] + C[i] == 3) 
        if i < 20:
            model += ((A[i] == 1).implies(A[i+1] == 0))
            model += ((B[i] == 1).implies(B[i+1] == 0))
            model += ((C[i] == 1).implies(C[i+1] == 0))

        model += ( ((A[i] == 1) | (A[i] == 2) ).implies(playedA[i] == 1),
                   ((B[i] == 1) | (B[i] == 2) ).implies(playedB[i] == 1),
                   ((C[i] == 1) | (C[i] == 2) ).implies(playedC[i] == 1)
                   )
    model += (sum(playedA) == num_played[0],
              sum(playedB) == num_played[1],
              sum(playedC) == num_played[2])

    return model

def get_model():
  return ping_pong()

