#***************************************************************************************#
#               LSINF2275 - Data mining & Decision Making                               #
#                       Project 2: BlackJack                                            #
#                                                                                       #
#   Authors :   BAILLY Gabriel                                                          #
#               WAUTIER Lara                                                            #
#               ZONE Corentin                                                           #
#   Program :   DATS2M                                                                  #
#                                                                                       #
#   inspiration: https://www.askpython.com/python/examples/blackjack-game-using-python  #
#                                                                                       #
#***************************************************************************************#

from statistics import mean
import sys
sys.path.append('c:/users/gabba/appdata/local/packages/pythonsoftwarefoundation.python.3.8_qbz5n2kfra8p0/localcache/local-packages/python38/site-packages')
import gym
from gym import wrappers
import random
import numpy as np
from collections import defaultdict
import collections
import itertools
import pandas as pd 

#------------------------------------------------------------------------------

# --- Set up --- #
"""
Set:
    - blackjack environnement for simulations, 
    - random Q function and Policy 
    - empty list for rewards
    - discount factor gamma    
"""

env = gym.make('Blackjack-v0')
envSpace = env.action_space.n
Q = {}
Policy = {}
Rewards = {}
gamma = 0.8

# to define all possible states
playerSum = [i for i in range(4,22)]
dealerCard = [i for i in range(1,11)]
actions = [0,1]
acePlayer = [True, False]

# we set all initial Q-values and policy to zero and one has we can do it arbitrarily
for p in playerSum:
    for d in dealerCard:
        for ace in acePlayer:
            for a in actions:
                Q[( (p,d,ace) , a )] = 0
                Policy[ (p,d,ace) ] = 1  

# game simulation when following current/updated policy 
def play(env, policy):
    """
    Game simulation when following current/updated policy
    """
    episode = []
    state = env.reset()
    while True:
        action = Policy[state]
        next_state, reward, done, info = env.step(action)
        episode.append((state, action, reward))
        state = next_state
        if done:
            break
    return episode

# IMPORTANT : makes iteration over dictionnaries pairs easier for arg max !
def pairwise(dico):
    "dico = (s0,s1,s2,s3,...) -> split into (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(dico)
    return zip(a, a)

def argMax(Q, Policy):
    """
    Returns best action a in A for maximizing the Q-value.
    """
    for j in pairwise(Q.keys()):
        state = j[0][0]
        maxQ = max(Q[(state,0)], Q[(state,1)])
        if maxQ == Q[(state,0)]:
            Policy[state] = 0
        else:
            Policy[state] = 1
    return Policy

#------------------------------------------------------------------------------

# --- Main Monte-Carlo Algorithm --- #

def monteCarloQ(env, N, Q, Policy, Rewards):
    """
    Computes the Q-values and the optimal policy for a Blackjack game.
    """
    
    ## loop "forever":
    for i in range(N):
        episode = play(env, Policy) # simulate 1 episode
        G = 0
        
        ## Go through all steps of episode
        for step in reversed(episode):                   
            G = gamma*G + step[2]  # remplacer gamma*G par gamma*Q si possible

            ## update Q-values
            if (step[0],step[1]) not in Rewards:        
                Rewards[(step[0] , step[1])] = [G]
                Q[(step[0] , step[1])] = G
            else:                               
                Rewards[(step[0],step[1])].append(G)
                Q[(step[0],step[1])] = (1/(len(Rewards[(step[0], step[1])])) * \
                                    sum(Rewards[(step[0],step[1])]))
            
            Policy = argMax(Q, Policy) # once episode is done, update policy
            
    return Q , Policy , Rewards
    
# --- Simulations --- #
Result = monteCarloQ(env, 1000000, Q, Policy, Rewards)
print(Result[0])
print(Result[1].keys())

#------------------------------------------------------------------------------
"""
Here we export the results to dataframes (we use R for visualization).
"""
# --- Export Q-value functions (if ace) --- #

Qlist = []
for key, value in Result[0].items():
    temp = [key,value]
    Qlist.append(temp)

## ace = True
Qtrue = []
for i in range(0,720,4):
    Qtrue.append(Qlist[i])
    Qtrue.append(Qlist[i+1])
    
qtrue = []
for i in range(0,360,2):
    maxTrue = max(Qtrue[i][1] , Qtrue[i+1][1])
    if maxTrue == Qtrue[i][1]:
        qtrue.append(Qtrue[i])
    else: 
        qtrue.append(Qtrue[i+1]) 
print(qtrue)    

dfQtrue = []
for i in range(18):
    dfQtrue.append([])
    for j in range(10):
        dfQtrue[i].append(qtrue[10*i+j][1])

dfQT = pd.DataFrame(data=dfQtrue)
dfQT.to_csv('Q-values true.csv') 

## ace = False
Qfalse = []
for i in range(2,721,4):
    Qfalse.append(Qlist[i])
    Qfalse.append(Qlist[i+1])

qfalse = []
for i in range(2,360,2):
    maxFalse = max(Qtrue[i][1] , Qtrue[i+1][1])
    if maxFalse == Qfalse[i][1]:
        qfalse.append(Qfalse[i])
    else: 
        qfalse.append(Qfalse[i+1]) 
print(qfalse)    

dfQfalse = []
for i in range(18):
    dfQfalse.append([])
    for j in range(10):
        dfQfalse[i].append(qfalse[10*i+j][1]) # TODO : solve bug :/

dfQF = pd.DataFrame(data=dfQfalse)
dfQF.to_csv('Q-values false.csv') 


# --- Export policy --- # 

optPolicy = []
for key, value in Result[1].items():
    temp = [key,value]
    optPolicy.append(temp)

## ace = True
poltrue = []
for i in range(0,360,2):
    poltrue.append(optPolicy[i])
polT = pd.DataFrame(data=poltrue)
polT.to_csv('policy true.csv') 
    
## ace = False
polfalse = []
for i in range(1,360,2):
    polfalse.append(optPolicy[i])
polF = pd.DataFrame(data=polfalse)
polF.to_csv('policy false.csv') 