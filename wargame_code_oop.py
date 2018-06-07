import itertools
from random import shuffle


class Deck:
    """Creates a deck of cards for the game, and methods for shuffling and dealing cards to players"""

    def __init__(self):
        value = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suit = ['Spades', 'Diamonds', 'Hearts', 'Clubs']

        self.cards = list(itertools.product(value,suit))

    def shuffle(self):
        shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0)


class Hand(Deck):
    """Defines the value of each card in the deck.  Also creates 2 lists of cards for each player: the face-down "stack" that is dealt from the dealer and the "win_pile" where winning cards from each round are stored."""

    def __init__(self):
        Deck.__init__(self)
        self.stack = []
        self.win_pile = []

    def card_value(self, card):
        value = card[0]
        total = 0
        if value == "J":
            total = 11
        elif value == "Q":
            total = 12
        elif value == "K":
            total = 13
        elif value == "A":
            total = 14
        else:
            total = int(value)
        return total

    def add_card(self,card):
        self.stack.append(card)

    def play_card(self):
        return self.stack.pop(0)

    def win_card(self, card):
        self.win_pile.append(card)


class Player(Hand):
    """Creates a player that is dealt cards for playing the game"""

    def __init__(self, name):
        Hand.__init__(self)
        self.name = name


class WarGame:
    """Creates a War Game class to store all of the card game methods"""

    def __init__(self):
        self.deck = Deck()
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

    def player_names(self):
        self.player1.name = input("Player 1, what is your name?  ")
        self.player2.name = input("Player 2, what is your name?  ")
        print("\n")

    def deal_all_cards(self):
        self.deck.shuffle()
        while len(self.deck.cards) > 0:
            self.player1.add_card(self.deck.deal_card())
            self.player2.add_card(self.deck.deal_card())

    def play_round(self):
        # Each player plays a card and the player with the highest card value wins the round.  Winning cards are stored in the players' "win_pile".
        if len(self.player1.stack) > 0 and len(self.player2.stack) > 0:
            # Players play a card as long as they have cards left in their "stack".
            P1_card = self.player1.play_card()
            P2_card = self.player2.play_card()
            print(self.player1.name, "your card is:", P1_card)
            print(self.player2.name, "your card is:", P2_card)
            if self.player1.card_value(P1_card) > self.player2.card_value(P2_card):
                print(self.player1.name, "is the winner of the round!")
                print("\n")
                self.player1.win_card(P1_card)
                self.player1.win_card(P2_card)
                self.play_round()
            elif self.player2.card_value(P2_card) > self.player1.card_value(P1_card):
                print(self.player2.name, "is the winner of the round!")
                print("\n")
                self.player2.win_card(P1_card)
                self.player2.win_card(P2_card)
                self.play_round()
            else:
            # War cards are stored in the "war_stack" and passed into the "war_battle" method.
                self.player1.card_value(P1_card) == self.player2.card_value(P2_card)
                print("Cards are of equal value.  This means war!!!")
                print("\n")
                war_stack = [P1_card, P2_card]
                self.war_battle(war_stack)
        else:
            self.game_winner()

    def war_battle(self, war_stack):
        if len(self.player1.stack) < 2 and len(self.player2.stack) <2:
        # A "war_battle" requires 2 cards to be played (1 face-down and 1 face-up).  If the players do not have enough cards to play, a winner is determined before the players' "stacks" are empty.
            self.game_winner()
        else:
        # The player with the highest "war_card" wins all the cards from the "war_battle".  This includes the "war_cards", the "face_down" cards and the cards in the "war_stack".
            P1_face_down = self.player1.play_card()
            P1_war_card = self.player1.play_card()
            P2_face_down = self.player2.play_card()
            P2_war_card = self.player2.play_card()
            print(self.player1.name,"your war card is:", P1_war_card)
            print(self.player2.name,"your war card is:", P2_war_card)
            if self.player1.card_value(P1_war_card) > self.player2.card_value(P2_war_card):
                print(self.player1.name, "is the winner of the war!")
                print('\n')
                self.player1.win_card(P1_face_down)
                self.player1.win_card(P1_war_card)
                self.player1.win_card(P2_face_down)
                self.player1.win_card(P2_war_card)
                for i in range(len(war_stack)):
                    self.player1.win_card(war_stack[i])
                self.play_round()
            elif self.player2.card_value(P2_war_card) > self.player1.card_value(P1_war_card):
                print(self.player2.name, "is the winner of the war!")
                print('\n')
                self.player2.win_card(P1_face_down)
                self.player2.win_card(P1_war_card)
                self.player2.win_card(P2_face_down)
                self.player2.win_card(P2_war_card)
                for i in range(len(war_stack)):
                    self.player2.win_card(war_stack[i])
                self.play_round()
            else:
            # If the players' "war_cards" are of equal value, another "war_battle" is played.
                self.player1.card_value(P1_war_card) == self.player2.card_value(P2_war_card)
                print("War cards are of equal value.  This means another war!!!")
                print("\n")
                self.war_battle()
                war_stack.append(P1_face_down)
                war_stack.append(P1_war_card)
                war_stack.append(P2_face_down)
                war_stack.append(P2_war_card)
                self.war_battle(war_stack)
                self.game_winner()

    def game_winner(self):
        # The player with the most cards in their "win_pile" wins the game.
        if len(self.player1.stack) == 0 or len(self.player2.stack) == 0:
            print("All cards have been played.")
            if len(self.player1.win_pile) > len(self.player2.win_pile):
                print(self.player1.name, "has the most cards and is the winner of the game.  Congratulations!!")
                print("\n")
                self.play_again()
            elif len(self.player1.win_pile) < len(self.player2.win_pile):
                print(self.player2.name, "has the most cards and is the winner of the game.  Congratuations!!")
                print("\n")
                self.play_again()
            else:
                len(self.player1.win_pile) == len(self.player2.win_pile)
                print(self.player1.name, " and ", self.player2.name, " have the same number of cards. ")
                print("Game ends in a tie. Nobody wins.")
                print("\n")
                self.play_again()

    def play_again(self):
        choice = input("Would you like to play another game? 1) Yes 2) No   ")
        if choice == "1":
            print("\n")
            print("Starting new game.")
            print("\n")
            self.deck = Deck()
            self.player1 = Player("Player 1")
            self.player2 = Player("Player 2")
            self.start()
        elif choice == "2":
            print("\n")
            print("Thanks for playing War!")
            print("\n")
            quit()

    def start(self):
        self.player_names()
        self.deal_all_cards()
        self.play_round()


game = WarGame()
game.start()
