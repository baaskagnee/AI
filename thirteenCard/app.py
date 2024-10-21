import tkinter as tk
from tkinter import messagebox, Canvas
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

    def deal(self):
        hands = [[] for _ in range(2)]  # Create empty hands for each player
        for index, card in enumerate(self.cards):
            player_index = index % 2  # Use num_players for distribution
            if index < 26:
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

        # Opponent's hand
        self.opponent_label = tk.Label(root, text="Opponent's Hand")
        self.opponent_label.pack()
        self.opponent_hand_frame = tk.Frame(root)
        self.opponent_hand_frame.pack(pady=10)

        # Played cards display
        self.played_cards_frame = tk.Frame(root)
        self.played_cards_frame.pack(pady=20)

        # Your hand
        self.player_hand_label = tk.Label(root, text="Your Hand")
        self.player_hand_label.pack()
        self.hand_frame = tk.Frame(root)
        self.hand_frame.pack(pady=10)

        self.play_button = tk.Button(root, text="Play Card", command=self.play_card, state=tk.DISABLED)
        self.play_button.pack(pady=10)

        self.selected_card_label = tk.Label(root, text="")
        self.selected_card_label.pack(pady=10)

        self.selected_cards = []  # Сонгосон картуудын жагсаалт
        self.deck = Deck()
        self.players = []

    def start_game(self):
        self.start_button.config(state=tk.DISABLED)
        hands = self.deck.deal()
        self.players = [Player(f'Player {i+1}', hand) for i, hand in enumerate(hands)]
        self.table = Table(self.players)  # Initialize the table with players
        self.current_player = 0
        self.update_ui()

    def update_ui(self):
        player = self.players[self.current_player]
        opponent = self.players[(self.current_player + 1) % len(self.players)]
        self.player_label.config(text=f"{player.name}'s Turn")
        self.show_hand(opponent, self.opponent_hand_frame)
        self.show_hand(player, self.hand_frame)

    def show_hand(self, player, frame):
        # Clear the previous hand display
        for widget in frame.winfo_children():
            widget.destroy()

        # Display the player's hand
        for i, card in enumerate(player.hand):
            if player == self.players[self.current_player]:
                # Show the actual cards for the current player
                image = Image.open(card.image_path)
                # Resize the card image
                image = image.resize((60, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                # Display the card image as a button for the current player
                card_button = tk.Button(frame, image=photo, command=lambda c=card: self.toggle_card_selection(c))
                card_button.image = photo  # Prevent garbage collection
                card_button.grid(row=0, column=i)
            else:
                # Show the back of the card for the opponent
                image = Image.open('cards/card_back.png')
                # Resize the card image
                image = image.resize((60, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                card_label = tk.Label(frame, image=photo)
                card_label.image = photo  # Prevent garbage collection
                card_label.grid(row=0, column=i)

    def toggle_card_selection(self, card):
        if card in self.selected_cards:
            self.selected_cards.remove(card)  # Хэрэв карт жагсаалтад байгаа бол устгана
        else:
            self.selected_cards.append(card)  # Шинээр карт сонгох үед жагсаалтад нэмнэ

        # Сонгосон картуудын жагсаалтыг харуулах
        self.selected_card_label.config(text=f"Selected: {', '.join(map(str, self.selected_cards))}")

        # Хэрэв сонгосон картууд байгаа бол Play товчийг идэвхжүүлнэ
        if self.selected_cards:
            self.play_button.config(state=tk.NORMAL)
        else:
            self.play_button.config(state=tk.DISABLED)

    def play_card(self):
        player = self.players[self.current_player]
        for card in self.selected_cards:
            if card in player.hand:
                self.table.place_card(player, card)  # Place the card on the table
        self.selected_card_label.config(text=f"Played: {', '.join(map(str, self.selected_cards))}")
        self.selected_cards.clear()  # Сонгосон картуудыг арилгана
        self.play_button.config(state=tk.DISABLED)  # Play товчийг идэвхгүй болгоно
        self.current_player = (self.current_player + 1) % len(self.players)
        self.update_ui()

        # Update the played cards display
        self.update_played_cards()

    def update_played_cards(self):
        # Clear the frame before displaying new cards
        for widget in self.played_cards_frame.winfo_children():
            widget.destroy()

        for i, card in enumerate(self.table.played_cards):
            # Картын зургийг ачаалах
            image = Image.open(card.image_path)
            image = image.resize((60, 100), Image.LANCZOS)  # Хэмжээг багасгах
            photo = ImageTk.PhotoImage(image)

            # Картын зургийг Tkinter интерфейс дээр харуулах
            card_label = tk.Label(self.played_cards_frame, image=photo)
            card_label.image = photo  # Эх сурвалжийн зургийг хадгалах (GC-ээс хамгаалах)
            card_label.grid(row=0, column=i)

# Тоглоомыг эхлүүлэх
if __name__ == "__main__":
    root = tk.Tk()
    game = ThirteenGameGUI(root)
    root.mainloop()
