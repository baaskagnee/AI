import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Define card suits and values
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
        self.image_path = f'cards/{value}_of_{suit}.png'

    def __repr__(self):
        return f'{self.value} of {self.suit}'

class Deck:
    def __init__(self):
        self.cards = [Card(value, suit) for value in VALUES for suit in SUITS]
        random.shuffle(self.cards)

    def deal(self):
        return [self.cards[:26], self.cards[26:]]

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def play_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return card
        return None

    def sort_hand(self):
        self.hand.sort(key=lambda card: (VALUES[card.value], SUITS[card.suit]))

class Table:
    def __init__(self):
        self.played_cards = []

    def place_card(self, player, card):
        if card in player.hand:
            player.play_card(card)
            self.played_cards.append(card)

    def start_new_round(self):
        self.played_cards.clear()

class CardMan:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
        self.opponent_hand = []

    def play_turn(self, opponent_played_cards):
        if opponent_played_cards:
            if len(opponent_played_cards) == 5:
                possible_cards = self.find_best_sequence()
                if possible_cards:
                    return possible_cards
            else:
                opponent_card_value = VALUES[opponent_played_cards[0].value]
                higher_cards = [card for card in self.hand if VALUES[card.value] > opponent_card_value]
                if higher_cards:
                    best_card = min(higher_cards, key=lambda card: VALUES[card.value])
                    self.hand.remove(best_card)
                    return [best_card]
                
        if len(self.hand) <= len(self.opponent_hand):
            return "pass"
        else:
            lowest_card = min(self.hand, key=lambda card: VALUES[card.value])
            self.hand.remove(lowest_card)
            return [lowest_card]

    def find_best_sequence(self):
        sorted_hand = sorted(self.hand, key=lambda card: (VALUES[card.value], SUITS[card.suit]))
        for i in range(len(sorted_hand) - 4):
            sequence = sorted_hand[i:i+5]
            validator = FiveCardValidator(sequence)
            if validator.is_sequence() and validator.is_same_suit():
                for card in sequence:
                    self.hand.remove(card)
                return sequence
        return None

    def evaluate_move(self):
        return len(self.hand)
    
    def pass_turn(self):
        return []

class FiveCardValidator:
    def __init__(self, cards):
        self.cards = cards

    def is_sequence(self):
        values = sorted([VALUES[card.value] for card in self.cards])
        return all(values[i] + 1 == values[i + 1] for i in range(len(values) - 1))

    def is_same_suit(self):
        return all(card.suit == self.cards[0].suit for card in self.cards)

class ThirteenGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Thirteen Card Game")
        self.root.geometry("1000x800")

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        self.player_label = tk.Label(root, text="")
        self.player_label.pack(pady=10)

        self.opponent_label = tk.Label(root, text="Opponent's Hand")
        self.opponent_label.pack()
        self.opponent_hand_frame = tk.Frame(root)
        self.opponent_hand_frame.pack(pady=10)

        self.played_cards_frame = tk.Frame(root)
        self.played_cards_frame.pack(pady=20)

        self.player_hand_label = tk.Label(root, text="Your Hand")
        self.player_hand_label.pack()
        self.hand_frame = tk.Frame(root)
        self.hand_frame.pack(pady=10)

        self.play_button = tk.Button(root, text="Play Card", command=self.play_card, state=tk.DISABLED)
        self.play_button.pack(pady=10)

        self.pass_button = tk.Button(root, text="Pass", command=self.pass_card)
        self.pass_button.pack(pady=10)

        self.selected_card_label = tk.Label(root, text="")
        self.selected_card_label.pack(pady=10)

        self.selected_cards = []
        self.deck = Deck()
        self.players = []

    def start_game(self):
        self.start_button.config(state=tk.DISABLED)
        hands = self.deck.deal()
        self.players = [
            Player('You', hands[0]),
            Player('CardMan', hands[1])
        ]
        for player in self.players:
            player.sort_hand()

        lowest_card_player = self.find_lowest_card_player()
        print(f"Player with the lowest card: {lowest_card_player} starts the game.")
        self.current_player = next(i for i, player in enumerate(self.players) if player.name == lowest_card_player)
        
        # Automatically play the first card of the starting player
        self.play_card()
        self.update_ui()
        # lowest_card_player = self.find_lowest_card_player()
        # print(lowest_card_player)
        # self.current_player = next(i for i, player in enumerate(self.players) if player.name == lowest_card_player)  # Эхлэх тоглогчийг тохируулах
        # self.play_card()

        # self.update_ui()
        # print(f"Хамгийн бага хөзөртэй тоглогч: {lowest_card_player} эхэлж байна.")
        # self.play_card()
    def find_lowest_card_player(self):
        lowest_card_player = None
        lowest_card_value = None

        for player in self.players:
            # Check if the player has cards in hand
            if player.hand:
                # Get the first card in their sorted hand (lowest card)
                first_card = player.hand[0]
                card_value = VALUES[first_card.value]

                # If this card has the lowest value encountered so far, update lowest_card_player
                if lowest_card_value is None or card_value < lowest_card_value:
                    lowest_card_value = card_value
                    lowest_card_player = player.name

        return lowest_card_player

    def update_ui(self):
        player = self.players[self.current_player]
        opponent = self.players[(self.current_player + 1) % len(self.players)]
        self.player_label.config(text=f"{player.name}'s Turn")
        self.show_hand(opponent, self.opponent_hand_frame)
        self.show_hand(player, self.hand_frame)

    def show_hand(self, player, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        for i, card in enumerate(player.hand):
            if player == self.players[self.current_player]:
                image = Image.open(card.image_path)
                image = image.resize((60, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                card_button = tk.Button(frame, image=photo, command=lambda c=card: self.toggle_card_selection(c))
                card_button.image = photo
                card_button.grid(row=0, column=i)
            else:
                image = Image.open('cards/card_back.png')
                image = image.resize((60, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                card_label = tk.Label(frame, image=photo)
                card_label.image = photo
                card_label.grid(row=0, column=i)

    def toggle_card_selection(self, card):
        if card in self.selected_cards:
            self.selected_cards.remove(card)
        else:
            self.selected_cards.append(card)

        self.selected_card_label.config(text=f"Selected: {', '.join(map(str, self.selected_cards))}")
        self.play_button.config(state=tk.NORMAL if self.selected_cards else tk.DISABLED)

    def pass_card(self):
        self.selected_cards.clear()
        self.current_player = (self.current_player + 1) % len(self.players)
        self.update_ui()

    def play_card(self):
        player = self.players[self.current_player]
        
        if len(self.selected_cards) not in {1, 2, 3, 5}:
            self.selected_card_label.config(text="Invalid selection. Choose 1, 2, 3, or 5 cards.")
            return

        if len(self.selected_cards) == 5:
            

        for card in self.selected_cards:
            self.table.place_card(player, card)

        self.selected_cards.clear()
        self.current_player = (self.current_player + 1) % len(self.players)
        self.update_ui()

# Main code to start the GUI
if __name__ == "__main__":
    root = tk.Tk()
    game_gui = ThirteenGameGUI(root)
    root.mainloop()
