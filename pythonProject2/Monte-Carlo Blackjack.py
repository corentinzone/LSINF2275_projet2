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


#------------------------------------------------------------------------------

env = gym.make('Blackjack-v0')

def play_episode(env):
    """
    Plays a single episode with a set policy in the environment given. Records the state, action 
    and reward for each step and returns the all timesteps for the episode.
    """
    episode = []
    state = env.reset()
    while True:
        probs = [0.8, 0.2] if state[0] > 18 else [0.2, 0.8]
        action = np.random.choice(np.arange(2), p=probs)
        next_state, reward, done, info = env.step(action)
        episode.append((state, action, reward))
        state = next_state
        if done:
            break
    return episode


# --- Main Monte-Carlo Algorithm --- #

def monteCarloQ(env, N):
    """
    Computes the Q-values and the optimal policy for a Blackjack game.
    """
    ## Set up
    envSpace = env.action_space.n
    Q_k_a = defaultdict(lambda: np.zeros(envSpace))
    Policy = np.zeros(280)
    Rewards = {}
    gamma = 0.9
    
    # -- Main Loop -- #
    
    ## Run episodes
    for i in range(N):
        res = play_episode(env) # simulate 1 episode
        G = 0
        ## Go through all steps of episode
        for j in range(len(res)):                   
            G = gamma * G + res[j][2]  # remplacer gamma*G par gamma*Q si possible
            
            if (res[j][0],res[j][1]) not in Rewards:        # create if not yet in there
                Rewards[(res[j][0],res[j][1])] = [G]
                Q_k_a[(res[j][0],res[j][1])] = G
            else:                               # append if already in there + average
                Rewards[(res[j][0],res[j][1])].append(G)
                Q_k_a[(res[j][0],res[j][1])] = (1/(len(Rewards[(res[j][0],res[j][1])])) * \
                                    sum(Rewards[(res[j][0],res[j][1])]))
                                    
    return Q_k_a
    
    
Qvalues = monteCarloQ(env, 50000)
print(Qvalues)
print(Qvalues.keys())
print(Qvalues.get(((11, 2, False), 0)))
print(Qvalues.get(((11, 2, False), 1)))
print(Qvalues.get(((16, 7, False), 0)))
print(Qvalues.get(((16, 7, False), 1)))
sorteddico=collections.OrderedDict(sorted(Qvalues.items()))
print(sorteddico)




