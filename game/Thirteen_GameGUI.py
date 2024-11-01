import tkinter as tk
from tkinter import messagebox, Canvas
import random
from PIL import Image, ImageTk  # Pillow-г импортлох

# Картуудын утга болон өнгийг тодорхойлох
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
        self.cards = []
        for value in VALUES:
            for suit in SUITS:
                card = Card(value, suit)
                self.cards.append(card)
        random.shuffle(self.cards)

    def deal(self):
        hands = [[] for _ in range(2)]  # Create empty hands for each player
        for index, card in enumerate(self.cards):
            player_index = index % 2
            if index < 26:
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

class Table:
    def __init__(self, players):
        self.players = players
        self.played_cards = []

    def place_card(self, player, card):
        if card in player.hand:
            player.play_card(card)
            self.played_cards.append(card)
        else:
            print(f"Card {card} not found in {player.name}'s hand.")

    def start_new_round(self):
        self.played_cards.clear()

    def show_played_cards(self):
        if not self.played_cards:
            return "No cards have been played yet."
        return ', '.join(map(str, self.played_cards))

    def reset_table(self):
        self.played_cards.clear()

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

    def find_lowest_card_player(self):
        lowest_card_player = None
        lowest_card_value = None

        for player in self.players:
            if player.hand:
                first_card = player.hand[0]
                card_value = VALUES[first_card.value]
                if lowest_card_value is None or card_value < lowest_card_value:
                    lowest_card_value = card_value
                    lowest_card_player = player.name

        return lowest_card_player

    def start_game(self):
        self.start_button.config(state=tk.DISABLED)
        hands = self.deck.deal()
        self.players = [
            Player('Хүн', hands[0]),
            Player('Машин', hands[1])
        ]

        for player in self.players:
            player.sort_hand()
        self.table = Table(self.players)
        self.current_player = 0
        self.update_ui()
        
        lowest_card_player = self.find_lowest_card_player()
        self.current_player = next(i for i, player in enumerate(self.players) if player.name == lowest_card_player)
        self.play_card()

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
        if self.selected_cards:
            self.play_button.config(state=tk.NORMAL)
        else:
            self.play_button.config(state=tk.DISABLED)

    def pass_card(self):
        self.table.played_cards.clear()
        self.selected_cards.clear()
        self.current_player = (self.current_player + 1) % len(self.players)
        self.update_ui()
        self.update_played_cards()

    def play_card(self):
        player = self.players[self.current_player]
        if not self.table.played_cards:
            if len(self.selected_cards) == 1:
                card = self.selected_cards[0]
                if card in player.hand:
                    self.table.place_card(player, card)
                else:
                    self.selected_cards.clear()
                    return
            elif len(self.selected_cards) == 2:
                card1, card2 = self.selected_cards
                if card1 in player.hand and card2 in player.hand and card1.value == card2.value:
                    self.table.place_card(player, card1)
                    self.table.place_card(player, card2)
                else:
                    self.selected_cards.clear()
                    return
            elif len(self.selected_cards) == 3:
                card1, card2, card3 = self.selected_cards
                if card1 in player.hand and card2 in player.hand and card3 in player.hand and \
                        card1.value == card2.value == card3.value:
                    self.table.place_card(player, card1)
                    self.table.place_card(player, card2)
                    self.table.place_card(player, card3)
                else:
                    self.selected_cards.clear()
                    return
        else:
            if len(self.selected_cards) == len(self.table.played_cards) and \
                    all(VALUES[self.selected_cards[i].value] > VALUES[self.table.played_cards[i].value] 
                        for i in range(len(self.selected_cards))):
                for card in self.selected_cards:
                    if card in player.hand:
                        self.table.place_card(player, card)
                    else:
                        self.selected_cards.clear()
                        return
            else:
                self.selected_cards.clear()
                return

        if len(player.hand) == 0:
            print("Game over")
        else:
            self.selected_card_label.config(text=f"Played: {', '.join(map(str, self.selected_cards))}")
            self.selected_cards.clear()
            self.play_button.config(state=tk.DISABLED)
            self.current_player = (self.current_player + 1) % len(self.players)
            self.update_ui()
            self.update_played_cards()

    def update_played_cards(self):
        for widget in self.played_cards_frame.winfo_children():
            widget.destroy()

        played_cards_text = self.table.show_played_cards()
        played_cards_label = tk.Label(self.played_cards_frame, text=played_cards_text)
        played_cards_label.pack()


# Тоглоомыг эхлүүлэх
if __name__ == "__main__":
    root = tk.Tk()
    game = ThirteenGameGUI(root)
    root.mainloop()