import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk  # Pillow-г импортлох

# Картуудын утга болон өнгийг тодорхойлох
SUITS = ['spades', 'hearts', 'diamonds', 'clubs']
VALUES = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']

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

    def deal(self, num_players):
        hands = [[] for _ in range(num_players)]  # Create empty hands for each player
        for index, card in enumerate(self.cards):
            player_index = index % num_players  # Use num_players for distribution
            hands[player_index].append(card) 
        return hands

# Тоглогч class
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

# Table class for managing player hands and played cards
class Table:
    def __init__(self, players):
        self.players = players  # List of players at the table
        self.played_cards = []  # Cards played on the table

    def place_card(self, player, card):
        """Places a card from a player's hand on the table."""
        if card in player.hand:
            player.play_card(card)
            self.played_cards.append(card)
        else:
            print(f"Card {card} not found in {player.name}'s hand.")

    def show_played_cards(self):
        """Shows the cards played on the table."""
        if not self.played_cards:
            return "No cards have been played yet."
        return ', '.join(map(str, self.played_cards))

    def reset_table(self):
        """Clears the played cards from the table."""
        self.played_cards.clear()

    def show_player_hands(self):
        """Displays all players' hands."""
        for player in self.players:
            print(f"{player.name}'s hand: {player.show_hand()}")

# GUI for the game
class ThirteenGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Thirteen Card Game")
        self.root.geometry("1000x800")

        # Тоглоомын товч болон гарах картын мэдээллийг харуулах
        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        self.player_label = tk.Label(root, text="")
        self.player_label.pack(pady=10)

        self.hand_frame = tk.Frame(root)
        self.hand_frame.pack()

        self.play_button = tk.Button(root, text="Play Card", command=self.play_card, state=tk.DISABLED)
        self.play_button.pack(pady=10)

        self.selected_card_label = tk.Label(root, text="")
        self.selected_card_label.pack(pady=10)

        # Add a label to display played cards
        self.played_cards_label = tk.Label(root, text="Played Cards: None", wraplength=400, justify="left")
        self.played_cards_label.pack(pady=10)

        self.deck = Deck()
        self.players = []

    def start_game(self):
        self.start_button.config(state=tk.DISABLED)
        num_players = 4
        hands = self.deck.deal(num_players)
        self.players = [Player(f'Player {i+1}', hand) for i, hand in enumerate(hands)]
        self.table = Table(self.players)  # Initialize the table with players
        self.current_player = 0
        self.update_ui()

    def update_ui(self):
        player = self.players[self.current_player]
        self.player_label.config(text=f"{player.name}'s Turn")
        self.show_hand(player)
        self.update_played_cards()

    def show_hand(self, player):
        for widget in self.hand_frame.winfo_children():
            widget.destroy()

        for i, card in enumerate(player.hand):
            # Картын зургийг ачаалах
            image = Image.open(card.image_path)
            
            # Хэмжээг тохируулах (жишээ нь: 100x140 пиксель)
            image = image.resize((60, 100), Image.LANCZOS)  # Хэмжээг багасгах
            photo = ImageTk.PhotoImage(image)

            # Картын зургийг Tkinter интерфейс дээр харуулах
            card_button = tk.Button(self.hand_frame, image=photo, command=lambda c=card: self.select_card(c))
            card_button.image = photo  # Эх сурвалжийн зургийг хадгалах (GC-ээс хамгаалах)
            card_button.grid(row=0, column=i)

    def select_card(self, card):
        self.selected_card = card
        self.selected_card_label.config(text=f"Selected: {self.selected_card}")
        self.play_button.config(state=tk.NORMAL)

    def play_card(self):
        player = self.players[self.current_player]
        if self.selected_card in player.hand:
            self.table.place_card(player, self.selected_card)  # Place the card on the table
            self.selected_card_label.config(text=f"Played: {self.selected_card}")
            self.play_button.config(state=tk.DISABLED)
            self.current_player = (self.current_player + 1) % len(self.players)
            self.update_ui()

        # Update played cards label
        self.update_played_cards()

    def update_played_cards(self):
        """Updates the label that shows the played cards."""
        played_cards_text = self.table.show_played_cards()
        self.played_cards_label.config(text=f"Played Cards: {played_cards_text}")


# Тоглоомыг эхлүүлэх
if __name__ == "__main__":
    root = tk.Tk()
    game = ThirteenGameGUI(root)
    root.mainloop()
