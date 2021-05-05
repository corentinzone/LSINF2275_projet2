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

        # if Split
        if choice.upper() == 'SP':
            split = True
            both_hand_loose = 0

            if player_cards[0].card_value == 1 and player_cards[1].card_value == 11:
                player_cards[0].card_value = 11

            player_hand_split = [[] for i in range(2)]
            player_score_split = []
            player_hand_split[0].append(player_cards[0])
            player_hand_split[1].append(player_cards[1])
            player_hand_split[0].append(hit(deck))
            player_hand_split[1].append(hit(deck))
            player_score_split.append(player_hand_split[0][0].card_value + player_hand_split[0][1].card_value)
            player_score_split.append(player_hand_split[1][0].card_value + player_hand_split[1][1].card_value)

            if player_hand_split[0][0].card_value == 11 and player_hand_split[0][1].card_value == 11:
                player_hand_split[0][0].card_value = 1
                player_score_split[0] -= 10
            if player_hand_split[1][0].card_value == 11 and player_hand_split[1][1].card_value == 11:
                player_hand_split[1][0].card_value = 1
                player_score_split[1] -= 10

            print("PLAYER HAND 1: ")
            for card_str in player_hand_split[0]:
                print(card_str)
            print("PLAYER SCORE = ", player_score_split[0])
            print("PLAYER HAND 2: ")
            for card_str in player_hand_split[1]:
                print(card_str)
            print("PLAYER SCORE = ", player_score_split[1])

            mise1 = mise
            mise2 = mise

            for i in range(2):
                player_cards = player_hand_split[i]
                player_score = player_score_split[i]
                print()
                print("NOW PLAYING HAND " + str(i + 1) + ": ")
                for card_str in player_cards:
                    print(card_str)
                print("PLAYER SCORE = ", player_score)

                if i==1:
                    hand1 = True
                else:
                    hand1 = False
                game_decision(deck, player_cards, player_score, dealer_cards, opti_policy)
            break

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

            # Print player cards and score
            print("PLAYER CARDS: ")
            for card_str in player_cards:
                print(card_str)
            print("PLAYER SCORE = ", player_score)

        # if Stand
        if choice.upper() == 'S':
            break

        # if Double, only one hit but the bet is doubled
        if choice.upper() == 'D':
            if split:
                if hand1:
                    mise1 = mise * 2
                else:
                    mise2 = mise * 2
            else:
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

            # Print player cards and score
            print("PLAYER CARDS: ")
            for card_str in player_cards:
                print(card_str)
            print("PLAYER SCORE = ", player_score)
            break

    if not split:
        """# Check if player has a Blackjack (only two card for blackjack, else the game continue)
        if player_score == 21 and len(player_cards) == 2:
            print("PLAYER HAS A BLACKJACK")
            quit("""

        # Check if player busts
        if player_score > 21:
            print("PLAYER BUSTED!!! GAME OVER!!!")
            capital -= mise
            # old return None

    else:
        # Check if player busts during a split
        if player_score > 21 and both_hand_loose < 2:
            print("PLAYER BUSTED!!! ONE HAND LOOSE!!!")
            both_hand_loose += 1
        if player_score > 21 and both_hand_loose == 2:
            print("PLAYER BUSTED!!! BOTH HAND LOOSE!!!")
            capital -= 2 * mise

            #old return None


    result = (player_cards, player_score,choice)

    if split:
        result_split.append(result)
        return result_split
    else:
        return result


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

            # Print player cards and score
            print("PLAYER CARDS: ")
            for card_str in player_cards:
                print(card_str)
            print("PLAYER SCORE = ", player_score)

        # dealing to dealer
        card = hit(deck)
        dealer_cards.append(card)
        dealer_score += card.card_value

        # if both first two card are Ace, the first Ace value = 1
        if len(dealer_cards) == 2:
            if dealer_cards[0].card_value == 11 and dealer_cards[1].card_value == 11:
                dealer_cards[1].card_value = 1
                dealer_score -= 10

            # printing dealer hand, hide second card and score
            print("DEALER CARDS: ")
            if len(dealer_cards) == 1:
                print(dealer_cards[0])
                print("DEALER SCORE = ", dealer_score)
            else:
                print(dealer_cards[0])
                print("DEALER SCORE = ", dealer_score - dealer_cards[-1].card_value)

    # Player gets a blackjack
    if player_score == 21:
        print("PLAYER HAS A BLACKJACK!!!!")
        print("PLAYER WINS!!!!")
        capital += 1.5 * mise
        #
        return (player_score,len(player_cards),dealer_cards[0].card_value,"BJ",1.5*mise)

    ############################game decision#############################
    result = game_decision(deck, player_cards, player_score, dealer_cards, opti_policy)
    if not split:
        player_cards = result[0]
        player_score = result[1]
        choice = result[2]

        #if player loose
        if player_score>21:
            return (player_score-player_cards[-1].card_value,len(player_cards)-1,dealer_cards[0].card_value,choice,-mise)

    else:
        player_cards1 = result[0][0]
        player_cards2 = result[1][0]
        player_score1 = result[0][1]
        player_score2 = result[1][1]
        choice = result[0][2]
        # if player loose
        if player_score1 > 21:
            return (player_score1 - player_cards1[-1].card_value, len(player_cards1) - 1,dealer_cards[0].card_value, "Sp", -mise)
        if player_score2 > 21:
            return (player_score2 - player_cards2[-1].card_value, len(player_cards2) - 1, dealer_cards[0].card_value, "Sp", -mise)


    #####################################dealer phase############################
    while dealer_score < 17:
        print("DEALER DECIDES TO HIT.....")
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

    if not split:
        # print card
        print("PLAYER CARDS: ")
        for card_str in player_cards:
            print(card_str)
        print("PLAYER SCORE = ", player_score)

        print("DEALER CARDS: ")
        for card_str in dealer_cards:
            print(card_str)
        print("DEALER SCORE = ", dealer_score)

        ###############End game result###############
        # Dealer busts
        if dealer_score > 21:
            print("DEALER BUSTED!!! YOU WIN!!!")
            capital += mise
            #
            if choice=="S":
                return (player_score,len(player_cards),dealer_cards[0].card_value,choice,+mise)
            else:
                return (player_score - player_cards[-1].card_value, len(player_cards)-1, dealer_cards[0].card_value, choice, +mise)


            # Dealer gets a blackjack
        if dealer_score == 21 and len(dealer_cards) == 2:
            print("DEALER HAS A BLACKJACK!!! PLAYER LOSES")
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
            print("TIE GAME!!!!")
            if choice == "S":
                return (player_score, len(player_cards), dealer_cards[0].card_value, choice, 0)
            else:
                return ( player_score - player_cards[-1].card_value, len(player_cards) - 1, dealer_cards[0].card_value, choice,0)

        # Player Wins
        elif player_score > dealer_score:
            print("PLAYER WINS!!!")
            capital += mise
            if choice == "S":
                return (player_score, len(player_cards), dealer_cards[0].card_value, choice, +mise)
            else:
                return (
                player_score - player_cards[-1].card_value, len(player_cards) - 1, dealer_cards[0].card_value, choice,
                +mise)

            # Dealer Wins
        else:
            print("DEALER WINS!!!")
            capital -= mise
            if choice == "S":
                return (player_score, len(player_cards), dealer_cards[0].card_value, choice, -mise)
            else:
                return (
                player_score - player_cards[-1].card_value, len(player_cards) - 1, dealer_cards[0].card_value, choice,
                -mise)

    else:
        out=[]
        # print card
        print("PLAYER HAND 1: ")
        for card_str in player_cards1:
            print(card_str)
        print("PLAYER SCORE = ", player_score1)

        print("PLAYER HAND 2: ")
        for card_str in player_cards2:
            print(card_str)
        print("PLAYER SCORE = ", player_score2)

        print("DEALER CARDS: ")
        for card_str in dealer_cards:
            print(card_str)
        print("DEALER SCORE = ", dealer_score)

        ###############End game result###############
        # Dealer busts
        if dealer_score >= 21:
            if player_score1 <= 21 and player_score2 <= 21:
                print("DEALER BUSTED!!! YOU WIN!!!")
                capital += mise1 + mise2
                #
                out=[(player_score1 - player_cards1[-1].card_value, len(player_cards1) - 1,dealer_cards[0].card_value, choice, +mise1),
                     (player_score2 - player_cards2[-1].card_value, len(player_cards1) - 1,dealer_cards[0].card_value, choice, +mise2)]
            elif player_score1 >= 21 and player_score2 <= 21:
                print("DEALER BUSTED!!! HAND 1 LOOSE, HAND 2 WIN!!!")
                capital += -mise1 + mise2
                out = [(player_score1 - player_cards1[-1].card_value, len(player_cards1) - 1, dealer_cards[0].card_value,choice, -mise1),
                       (player_score2 - player_cards2[-1].card_value, len(player_cards1) - 1, dealer_cards[0].card_value,choice, +mise2)]
            else :
                print("DEALER BUSTED!!! HAND 1 WIN, HAND 2 LOOSE!!!")
                capital += mise1 - mise2
                out = [(player_score1 - player_cards1[-1].card_value, len(player_cards1) - 1, dealer_cards[0].card_value,choice, +mise1),
                       (player_score2 - player_cards2[-1].card_value, len(player_cards1) - 1, dealer_cards[0].card_value,choice, -mise2)]

        else:
            # Dealer gets a blackjack
            if dealer_score == 21 and len(dealer_cards) == 2:
                print("DEALER HAS A BLACKJACK!!! PLAYER LOSES")
                capital -= mise1 + mise2
                #
                out = [(player_score1 - player_cards1[-1].card_value, len(player_cards1) - 1,dealer_cards[0].card_value, choice, -mise1),
                       (player_score2 - player_cards2[-1].card_value, len(player_cards1) - 1,dealer_cards[0].card_value, choice, -mise2)]

            if player_score1 > 21:
                print("HAND 1: PLAYER BUSTED")
                capital -= mise1
                out = [(player_score1 - player_cards1[-1].card_value, len(player_cards1) - 1,dealer_cards[0].card_value, choice, -mise1)]
            else:
                if dealer_score == player_score1:
                    print("HAND 1: TIE GAME!!!!")
                    out = [(player_score1 - player_cards1[-1].card_value, len(player_cards1) - 1,dealer_cards[0].card_value, choice, 0)]
                if player_score1 < dealer_score:
                    print("HAND 1: DEALER WINS!!!")
                    capital -= mise1
                    out = [(player_score1 - player_cards1[-1].card_value, len(player_cards1) - 1,dealer_cards[0].card_value, choice, -mise1)]
                if player_score1 > dealer_score:
                    print("HAND 1: PLAYER WINS!!!")
                    capital += mise1
                    out = [(player_score1 - player_cards1[-1].card_value, len(player_cards1) - 1, dealer_cards[0].card_value,choice, mise1)]

            if player_score2 > 21:
                print("HAND 2: PLAYER BUSTED")
                capital -= mise2
                out.append((player_score2 - player_cards2[-1].card_value, len(player_cards2) - 1,dealer_cards[0].card_value, choice, -mise2))
            else:
                if dealer_score == player_score2:
                    print("HAND 2: TIE GAME!!!!")
                    out.append((player_score2 - player_cards2[-1].card_value, len(player_cards2) - 1,dealer_cards[0].card_value, choice, 0))
                if player_score2 < dealer_score:
                    print("HAND 2: DEALER WINS!!!")
                    capital -= mise2
                    out.append((player_score2 - player_cards2[-1].card_value, len(player_cards2) - 1,dealer_cards[0].card_value, choice, -mise2))
                if player_score2 > dealer_score:
                    print("HAND 2: PLAYER WINS!!!")
                    capital += mise2
                    out.append((player_score2 - player_cards2[-1].card_value, len(player_cards2) - 1,dealer_cards[0].card_value, choice, +mise2))
        return out


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
        output = game(deck_game,opti_policy)
        if len(output) == 5:
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

        if len(output) == 2:
            result_hand.extend(output)
            for i in range(2):
                G = output[i][4]
                if output[i][3] == "S":
                    mystrat = 0
                elif output[i][3] == "H":
                    mystrat = 1
                elif output[i][3] == "D":
                    mystrat = 2
                else:
                    mystrat = 3

                key_dico = (output[i][0], output[i][1], output[i][2], mystrat)
                if key_dico not in Rewards:
                    Rewards[key_dico] = [G]
                    Q_value[key_dico] = G
                else:
                    Rewards[key_dico].append(G)
                    Q_value[key_dico] = round((1 / len(Rewards[key_dico])) * sum(Rewards[key_dico]),5)

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
        return "H"

    else:
        # case Split (two cards have the same value)
        if (player_cards[0].card_value == player_cards[1].card_value or
            (player_cards[0].card_value == 1 and player_cards[1].card_value == 11)) and not split and len(
            player_cards) == 2:
            if situation_key in optimal_policy:
                out = np.random.choice(["H", "S", "D", "Sp", optimal_policy[situation_key][0]],
                                       p=[0.05, 0.05, 0.05, 0.05, 0.8])
            else:
                out = np.random.choice(["H", "S", "D", "Sp"])

        elif len(player_cards) == 2:
            if situation_key in optimal_policy:
                out = np.random.choice(["H", "S", "D", optimal_policy[situation_key][0]], p=[0.07, 0.07, 0.07, 0.79])
            else:
                out = np.random.choice(["H", "S", "D"])
        else:
            if situation_key in optimal_policy:
                out = np.random.choice(["H", "S", optimal_policy[situation_key][0]], p=[0.1, 0.1, 0.8])
            else:
                out = np.random.choice(["H", "S"])

    if out== 0:
        out = "S"
    elif out== 1:
        out == "H"
    elif out == 2:
        out == "D"
    elif out== 3:
        out == "SP"

    return out


def create_opti_policy(Q_value_sorted):
    opti_policy={}
    for key, value in Q_value_sorted.items():
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
    for i in range(5):
        myresult = monte_carlo(opti_policy)
        Q_value_sorted = collections.OrderedDict(sorted(myresult[2].items()))
        capital = myresult[0]
        per_win = myresult[3]
        print("CAPITAL FINAL : " + str(myresult[0][-1]))
        print("PERCENTAGE WIN: "+str(myresult[3]))
        opti_policy=create_opti_policy(Q_value_sorted)

        out.append([opti_policy,capital, per_win])

    return out

result = simulation()
print("PERCENTAGE WIN: "+str(result[0][2]))
print(result[0][0])
print("PERCENTAGE WIN: "+str(result[1][2]))
print(result[1][0])
print("PERCENTAGE WIN: "+str(result[-1][2]))
print(result[-1][0])