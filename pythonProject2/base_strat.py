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

# import
import random
import os
import collections

# Global variables
import numpy as np

suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
suits_values = {"Spades": "\u2664", "Hearts": "\u2661", "Clubs": "\u2667", "Diamonds": "\u2662"}
cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
cards_values = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10,
                "K": 10}
nb_deck = 4
result_split = []
global split

global capital
hand1 = True

def cls():
    os.system('cls')

class Card:
    def __init__(self, suit, value, card_value):
        self.suit = suit
        self.value = value
        self.card_value = card_value

    def __str__(self):
        return self.value + self.suit


def deck(nb_deck):
    a = 0
    deck = []
    while (a < nb_deck):
        for i in suits:
            for j in cards:
                deck.append(Card(suits_values[i], j, cards_values[j]))
        a += 1
    return deck


def hit(deck):
    card = deck[0]
    deck.remove(card)
    return card


def game_decision(deck, player_cards, player_score,dealer_cards,opti_policy):
    global split
    global both_hand_loose
    global capital
    global mise, mise1, mise2
    global hand1
    ################################Enter the choice of the player################################
    choice = "BJ"
    while player_score < 21:

        #random choice of the policy
        choice = choice_policy(player_cards,dealer_cards,opti_policy)

        # if hit
        if choice.upper() == 'H':
            card = hit(deck)
            player_cards.append(card)
            player_score += card.card_value

            # if ace among card
            c = 0
            while player_score > 21 and c < len(player_cards):
                if player_cards[c].card_value == 11:
                    player_cards[c].card_value = 1
                    player_score -= 10
                    c += 1
                else:
                    c += 1

        # if Stand
        if choice.upper() == 'S':
            break

        # if Double, only one hit but the bet is doubled
        if choice.upper() == 'D':
            mise = mise * 2
            card = hit(deck)
            player_cards.append(card)
            player_score += card.card_value

            # if ace among card
            c = 0
            while player_score > 21 and c < len(player_cards):
                if player_cards[c].card_value == 11:
                    player_cards[c].card_value = 1
                    player_score -= 10
                    c += 1
                else:
                    c += 1

            break


    """# Check if player has a Blackjack (only two card for blackjack, else the game continue)
    if player_score == 21 and len(player_cards) == 2:
        print("PLAYER HAS A BLACKJACK")
        quit("""

    # Check if player busts
    if player_score > 21:
        capital -= mise

    return (player_cards, player_score,choice)


def game(deck,opti_policy):
    global cards_values

    player_cards = []
    dealer_cards = []

    player_score = 0
    dealer_score = 0
    global split
    split = False
    global both_hand_loose
    global capital
    global mise

    ############dealing first two card to player and dealer################
    while len(player_cards) < 2:

        # dealing to player
        card = hit(deck)
        player_cards.append(card)
        player_score += card.card_value

        # if both first two card are Ace, the first Ace value = 1
        if len(player_cards) == 2:
            if player_cards[0].card_value == 11 and player_cards[1].card_value == 11:
                player_cards[0].card_value = 1
                player_score -= 10

        # dealing to dealer
        card = hit(deck)
        dealer_cards.append(card)
        dealer_score += card.card_value

        # if both first two card are Ace, the first Ace value = 1
        if len(dealer_cards) == 2:
            if dealer_cards[0].card_value == 11 and dealer_cards[1].card_value == 11:
                dealer_cards[1].card_value = 1
                dealer_score -= 10

    # Player gets a blackjack
    if player_score == 21:
        capital += 1.5 * mise
        #
        return (player_score,len(player_cards),dealer_cards[0].card_value,"BJ",1.5*mise)

    ############################game decision#############################
    result = game_decision(deck, player_cards, player_score, dealer_cards, opti_policy)

    player_cards = result[0]
    player_score = result[1]
    choice = result[2]

    #if player loose
    if player_score>21:
        return (player_score-player_cards[-1].card_value,len(player_cards)-1,dealer_cards[0].card_value,choice,-mise)


    #####################################dealer phase############################
    while dealer_score < 17:
        dealer_hit_card = hit(deck)
        dealer_cards.append(dealer_hit_card)
        dealer_score += dealer_hit_card.card_value

        # case if Ace in hand
        c = 0
        while dealer_score > 21 and c < len(dealer_cards):
            if dealer_cards[c].card_value == 11:
                dealer_cards[c].card_value = 1
                dealer_score -= 10
                c += 1
            else:
                c += 1


    ###############End game result###############
    # Dealer busts
    if dealer_score > 21:
        capital += mise
        #
        if choice=="S":
            return (player_score,len(player_cards),dealer_cards[0].card_value,choice,+mise)
        else:
            return (player_score - player_cards[-1].card_value, len(player_cards)-1, dealer_cards[0].card_value, choice, +mise)


        # Dealer gets a blackjack
    if dealer_score == 21 and len(dealer_cards) == 2:
        capital -= mise
        #
        if choice == "S":
            return (player_score, len(player_cards), dealer_cards[0].card_value, choice, -mise)
        else:
            return (
            player_score - player_cards[-1].card_value, len(player_cards) - 1, dealer_cards[0].card_value, choice,
            -mise)

    # TIE Game
    if dealer_score == player_score:
        if choice == "S":
            return (player_score, len(player_cards), dealer_cards[0].card_value, choice, 0)
        else:
            return ( player_score - player_cards[-1].card_value, len(player_cards) - 1, dealer_cards[0].card_value, choice,0)

    # Player Wins
    elif player_score > dealer_score:
        capital += mise
        if choice == "S":
            return (player_score, len(player_cards), dealer_cards[0].card_value, choice, +mise)
        else:
            return (
            player_score - player_cards[-1].card_value, len(player_cards) - 1, dealer_cards[0].card_value, choice,
            +mise)

        # Dealer Wins
    else:
        capital -= mise
        if choice == "S":
            return (player_score, len(player_cards), dealer_cards[0].card_value, choice, -mise)
        else:
            return (
            player_score - player_cards[-1].card_value, len(player_cards) - 1, dealer_cards[0].card_value, choice,
            -mise)



def monte_carlo(opti_policy):
    deck_game = deck(6)
    random.shuffle(deck_game)
    global capital
    global mise
    capital = 10000000
    out_capital = [capital]
    result_hand=[]
    per_win=[]
    nb_win=0

    #renforcement learning
    Q_value={}
    Rewards={}
    for key, value in opti_policy.items():
        key_Q = (key[0],key[1],value[0])
        Q_value[key_Q] = value[1]
        Rewards[key_Q] = [value[1]]

    ite = 0
    nb_ite = 10000


    while capital > 0 and ite < nb_ite:
        ite += 1
        #suffle deck if not enough cards present
        if len(deck_game)<=10:
            deck_game = deck(6)
            random.shuffle(deck_game)

        mise = 1
        #simule a game
        output = game(deck_game,opti_policy)
        result_hand.append(output)
        G = output[4]
        if output[3] == "S":
            mystrat = 0
        elif output[3] == "H":
            mystrat = 1
        elif output[3] == "D":
            mystrat = 2
        else:
            mystrat = 3
        key_dico = (output[0],output[2],mystrat)
        if key_dico not in Rewards:
            Rewards[key_dico] = [G]
            Q_value[key_dico] = G
        else:
            Rewards[key_dico].append(G)
            Q_value[key_dico] = round((1/len(Rewards[key_dico])) * sum(Rewards[key_dico]),5)

        out_capital.append(capital)

        if out_capital[ite-1] <= out_capital[ite]:
            nb_win+=1
        win = round((nb_win/ite),2)
        per_win.append(win)

    return [out_capital,result_hand,Q_value,per_win]


def choice_policy(player_cards,dealer_cards,optimal_policy):
    player_score = 0
    for i in player_cards:
        player_score += i.card_value
    situation_key = (player_score,dealer_cards[0].card_value)

    if player_score<=8:
        out = "H"

    else:
        if len(player_cards) == 2:
            if situation_key in optimal_policy.keys():
                out = np.random.choice(["H", "S", "D", optimal_policy[situation_key][0]], p=[0.07, 0.07, 0.07, 0.79])
            else:
                out = np.random.choice(["H", "S", "D"])
        else:
            if situation_key in optimal_policy.keys():
                out = np.random.choice(["H", "S", optimal_policy[situation_key][0]], p=[0.1, 0.1, 0.8])
            else:
                out = np.random.choice(["H", "S"])

    if out== 0:
        out = "S"
    elif out== 1:
        out == "H"
    elif out == 2:
        out == "D"

    return out


def create_opti_policy(Q_value_sorted):
    opti_policy={}
    for key, value in Q_value_sorted.items():
        if key[0]>=9 and key[1]!=1:
            key_opti = (key[0], key[1])
            if key_opti not in opti_policy:
                opti_policy[key_opti] = (key[2], value)
            else:
                if opti_policy[key_opti][1] < value:
                    opti_policy[key_opti] = (key[2], value)
    return opti_policy


def simulation():
    opti_policy={}
    out=[]
    for i in range(50):
        myresult = monte_carlo(opti_policy)
        Q_value_sorted = collections.OrderedDict(sorted(myresult[2].items()))
        capital = myresult[0]
        per_win = myresult[3]
        opti_policy=create_opti_policy(Q_value_sorted)

        out.append([opti_policy,capital, per_win])

    return out

result = simulation()
#print("PERCENTAGE WIN: "+str(result[0][2]))
print(result[0][0])
#print("PERCENTAGE WIN: "+str(result[1][2]))
print(result[1][0])
#print("PERCENTAGE WIN: "+str(result[-1][2]))
print(result[-1][0])