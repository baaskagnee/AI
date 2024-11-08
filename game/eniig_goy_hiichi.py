import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

# Define card values and suits
SUITS = {
    'diamonds': 1,
    'clubs': 2,
    'hearts': 3,
    'spades': 4
}

VALUES = {
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
    '2': 15
}

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.image_path = f'cards/{value}_of_{suit}.png'  # Update this path according to your card image locations

    def __repr__(self):
        return f'{self.value} of {self.suit}'

class Deck:
    def __init__(self):
        self.cards = []
        for value in VALUES:
            for suit in SUITS:
                card = Card(value, suit)
                self.cards.append(card)
        random.shuffle(self.cards)

    def deal(self):
        hands = [[] for _ in range(2)]  # Create empty hands for each player
        for index, card in enumerate(self.cards):
            player_index = index % 2  # Distribute cards to players
            if index < 26:  # Deal only half the deck
                hands[player_index].append(card)
        return hands

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def play_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return card
        else:
            return None

    def show_hand(self):
        return ', '.join(map(str, self.hand))
    
    def sort_hand(self):
        self.hand.sort(key=lambda card: (VALUES[card.value], SUITS[card.suit]))

class AICardManager(Player):
    def __init__(self, name, hand):
        super().__init__(name, hand)

# Main game logic
class Game:
    def __init__(self):
        self.deck = Deck()
        self.hands = self.deck.deal()
        self.human_player = Player("Human", self.hands[0])
        self.ai_player = AICardManager("Mochi", self.hands[1])
        self.players = [self.human_player, self.ai_player]

        # Sort hands for all players
        for player in self.players:
            player.sort_hand()

        # Find the player with the lowest card
        self.lowest_card_player = self.find_lowest_card_player()
        print(f"Хамгийн бага хөзөртэй тоглогч: {self.lowest_card_player} эхэлж байна.")
        self.current_player = next(i for i, player in enumerate(self.players) if player.name == self.lowest_card_player)

    def find_lowest_card_player(self):
        lowest_card_value = float('inf')
        lowest_card_player = None
        for player in self.players:
            player_lowest_card = min(VALUES[card.value] for card in player.hand)
            if player_lowest_card < lowest_card_value:
                lowest_card_value = player_lowest_card
                lowest_card_player = player.name
        return lowest_card_player

# Initialize the game
game = Game()
