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

# Global variables

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

cls = lambda: os.system('cls')

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


def game_decision(deck, player_cards, player_score):
    global split
    global both_hand_loose
    global capital
    global mise, mise1, mise2
    global hand1
    ################################Enter the choice of the player################################
    while player_score < 21:
        # case Split (two cards have the same value)
        if (player_cards[0].card_value == player_cards[1].card_value or
            (player_cards[0].card_value == 1 and player_cards[1].card_value == 11)) and not split:
            choice = input("(H)it or (S)tand or (D)ouble or (Sp)lit : ")
            # Sanity checks for player's choice
            while len(choice) not in [1, 2] or (
                    choice.upper() != 'H' and choice.upper() != 'S' and choice.upper() != 'D'
                    and choice.upper() != 'SP'):
                print("Wrong choice!! Try Again")
                choice = input("(H)it or (S)tand or (D)ouble or (Sp)lit : ")
        else:
            choice = input("(H)it or (S)tand or (D)ouble : ")
            # Sanity checks for player's choice
            while len(choice) != 1 or (choice.upper() != 'H' and choice.upper() != 'S' and choice.upper() != 'D'):
                print("Wrong choice!! Try Again")
                choice = input("(H)it or (S)tand or (D)ouble: ")

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
                game_decision(deck, player_cards, player_score)
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
            #
            return None
    else:
        # Check if player busts during a split
        if player_score > 21 and both_hand_loose < 2:
            print("PLAYER BUSTED!!! ONE HAND LOOSE!!!")
            both_hand_loose += 1
        if player_score > 21 and both_hand_loose == 2:
            print("PLAYER BUSTED!!! BOTH HAND LOOSE!!!")
            capital -= 2 * mise
            #
            return None

    result = (player_cards, player_score)

    if split:
        result_split.append(result)
        return result_split
    else:
        return result


def game(deck):
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
        return None

    ############################game decision#############################
    result = game_decision(deck, player_cards, player_score)
    if result != None:
        if not split:
            player_cards = result[0]
            player_score = result[1]
        else:
            player_cards1 = result[0][0]
            player_cards2 = result[1][0]
            player_score1 = result[0][1]
            player_score2 = result[1][1]
    else:
        return None

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
            return None

            # Dealer gets a blackjack
        if dealer_score == 21 and len(dealer_cards) == 2:
            print("DEALER HAS A BLACKJACK!!! PLAYER LOSES")
            capital -= mise
            #
            return None

        # TIE Game
        if dealer_score == player_score:
            print("TIE GAME!!!!")

        # Player Wins
        elif player_score > dealer_score:
            print("PLAYER WINS!!!")
            capital += mise

            # Dealer Wins
        else:
            print("DEALER WINS!!!")
            capital -= mise

    else:
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
                return None
            elif player_score1 >= 21 and player_score2 <= 21:
                print("DEALER BUSTED!!! HAND 1 LOOSE, HAND 2 WIN!!!")
                capital += -mise1 + mise2
            else :
                print("DEALER BUSTED!!! HAND 1 WIN, HAND 2 LOOSE!!!")
                capital += mise1 - mise2

        else:
            # Dealer gets a blackjack
            if dealer_score == 21 and len(dealer_cards) == 2:
                print("DEALER HAS A BLACKJACK!!! PLAYER LOSES")
                capital -= mise1 + mise2
                #
                return None

            if player_score1 > 21:
                print("HAND 1: PLAYER BUSTED")
                capital -= mise1
            else:
                if dealer_score == player_score1:
                    print("HAND 1: TIE GAME!!!!")
                if player_score1 < dealer_score:
                    print("HAND 1: DEALER WINS!!!")
                    capital -= mise1
                if player_score1 > dealer_score:
                    print("HAND 1: PLAYER WINS!!!")
                    capital += mise1

            if player_score2 > 21:
                print("HAND 2: PLAYER BUSTED")
                capital -= mise2
            else:
                if dealer_score == player_score2:
                    print("HAND 2: TIE GAME!!!!")
                if player_score2 < dealer_score:
                    print("HAND 2: DEALER WINS!!!")
                    capital -= mise2
                if player_score2 > dealer_score:
                    print("HAND 2: PLAYER WINS!!!")
                    capital += mise2


def multiple_game():
    deck_game = deck(6)
    random.shuffle(deck_game)
    global capital
    global mise
    capital = 1000
    play = True

    while capital > 0 and play:
        mise = 20
        game(deck_game)
        print("CAPITAL = "+str(capital))
        #continue game
        choice = input("CONTINUE: Y/N ")
        while len(choice) != 1 or (choice.upper() != 'Y' and choice.upper() != 'N'):
            print("Wrong choice!! Try Again")
            choice = input("CONTINUE: Y/N ")
        if choice.upper() == 'N':
            play = False
        cls()

multiple_game()
