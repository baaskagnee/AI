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
    def make_move(self,last_played_car):
        if self.hand:
            played_card = random.choice(self.hand)  # AI randomly plays a card
            print(f"AI selected card: {played_card}")  # Debug output
            return played_card  # Make sure to play and remove it from hand
        return None

    # def make_move(self, last_played_cards):
    #     card=[]
    #     """AI тоглогч хөдөлгөөн хийх."""
    #     if len(last_played_cards) == 5:  # Нөгөө тоглогчийн 5 хөзрөөр тоглосон эсэхийг шалгана
    #         card_combo = self.play_best_five_card_combo(last_played_cards)
    #         if card_combo:
    #             print(f"AI тоглогч тоглох 5 хөзрийн хослол: {card_combo}")
    #         else:
    #             print("AI тоглогч тоглох боломжгүй байна.")
    #     elif len(last_played_cards) == 3:  # Нөгөө тоглогчийн 3 карт тоглосон үед
    #         card_triple = self.play_best_triple(last_played_cards)
    #         if card_triple:
    #             print(f"AI тоглогч тоглох гурвалсан хослол: {card_triple}")
    #         else:
    #             print("AI тоглогч тоглох боломжгүй байна.")
    #     elif len(last_played_cards) == 2:  # Нөгөө тоглогчийн 2 карт тоглосон үед
    #         card_pair = self.play_best_pair(last_played_cards)
    #         if card_pair:
    #             print(f"AI тоглогч тоглох хослол: {card_pair}")
    #         else:
    #             print("AI тоглогч тоглох боломжгүй байна.")
    #     elif len(last_played_cards) == 1:
    #         # 1 карт тоглосон тохиолдолд өмнөх стратеги ашиглана
    #         card = self.play_best_card(last_played_cards)
    #         if card:
    #             print(f"AI тоглогч тоглох карт: {card}")
    #             return card
    #         else:
    #             print("AI тоглогч тоглох боломжгүй байна.")
    #             return None
    #     elif len(last_played_cards) == 0:
    #         card = self.hand[0]
    #         return card
    #     print("CARDS:",card)
    #     self.hand.remove(card)
    #     card.clear
    def play_best_card(self, last_played_card):
        """AI chooses the best card to play against a single opponent's card."""

        # Evaluate the last played card's value
        last_card_value = VALUES[last_played_card.value]

        # Find the smallest card that can beat the last played card
        for card in self.hand:
            if VALUES[card.value] > last_card_value:
                self.hand.remove(card)  # Remove the card from the hand after playing it
                return card  # Play this card
        
        # If no card can beat the last played card, return None to indicate a pass
        return None
    def play_best_triple(self, last_played_triple):
            """AI chooses the best triple (three of a kind) to play against the opponent's triple."""
            # Collect triples in hand
            triples = self.find_multiples(3)
            
            # Evaluate the last played triple's value
            last_triple_value = VALUES[last_played_triple[0].value]
             
            # Find the first stronger triple to play
            for triple in triples:
                if VALUES[triple[0].value] > last_triple_value:
                    for card in triple:
                        self.hand.remove(card)
                    return triple  # Play this triple
            
            return None  # No triple strong enough to play

    def play_best_pair(self, last_played_pair):
        """AI chooses the best pair to play against the opponent's pair."""
        # Collect pairs in hand
        pairs = self.find_multiples(2)
        
        # Evaluate the last played pair's value
        last_pair_value = VALUES[last_played_pair[0].value]
        
        # Find the first stronger pair to play
        for pair in pairs:
            if VALUES[pair[0].value] > last_pair_value:
                for card in pair:
                    self.hand.remove(card)
                return pair  # Play this pair
        
        return None  # No pair strong enough to play

    def find_multiples(self, count):
        """Helper function to find all groups of 'count' cards with the same value in hand."""
        multiples = []
        value_counts = {}

        # Count the occurrences of each card value in hand
        for card in self.hand:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1

        # Collect cards that meet the specified count criteria
        for value, cnt in value_counts.items():
            if cnt >= count:
                same_value_cards = [card for card in self.hand if card.value == value]
                multiples.append(same_value_cards[:count])

        return multiples

class Table:
    def __init__(self, players):
        self.players = players  # List of players at the table
        self.played_cards = []  # Cards played on the table

    def place_card(self, player, card):
        """Place a card from the player's hand on the table."""
        if card in player.hand:
            player.play_card(card)
            self.played_cards.append(card)
        else:
            print(f"Card {card} not found in {player.name}'s hand.")

    def start_new_round(self):
        """Start a new round by clearing the played cards."""
        self.played_cards.clear()

    def show_played_cards(self):
        """Display the cards played on the table."""
        if not self.played_cards:
            return "No cards have been played yet."
        return ', '.join(map(str, self.played_cards))
class ThirteenGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Card Game")
        self.root.geometry("1000x800")
        
        # UI Components
        self.player_label = tk.Label(root, text="")
        self.player_label.pack(pady=10)

        self.ai_label = tk.Label(root, text="AI's Hand")
        self.ai_label.pack()
        self.ai_hand_frame = tk.Frame(root)
        self.ai_hand_frame.pack(pady=10)

        self.played_cards_frame = tk.Frame(root)
        self.played_cards_frame.pack(pady=20)

        self.player_hand_label = tk.Label(root, text="Your Hand")
        self.player_hand_label.pack()
        self.hand_frame = tk.Frame(root)
        self.hand_frame.pack(pady=10)

        self.play_button = tk.Button(root, text="Play Card", command=self.play_card, state=tk.DISABLED)
        self.play_button.pack()

        self.pass_button = tk.Button(root, text="Pass", command=self.human_pass_card)
        self.pass_button.pack(pady=10)

        self.selected_cards = []  # Сонгосон картуудын жагсаалт
        self.players = []

        self.deck = Deck()
        self.hands = self.deck.deal()
        self.human_player = Player("Human", self.hands[0])
        self.ai_player = AICardManager("Mochi", self.hands[1])
        self.players = [self.human_player, self.ai_player]      

        for player in self.players:
            player.sort_hand()
        self.table = Table(self.players) 
        self.lowest_card_player = self.find_lowest_card_player()
        print(f"Хамгийн бага хөзөртэй тоглогч: {self.lowest_card_player} эхэлж байна.") 
        if  self.lowest_card_player == "Mochi":
            self.ai_play(self.table.played_cards)
            self.update_ui()
        else:
            self.update_ui()
    def find_lowest_card_player(self):
        lowest_card_value = float('inf')
        lowest_card_player = None
        for player in self.players:
            player_lowest_card = min(VALUES[card.value] for card in player.hand)
            if player_lowest_card < lowest_card_value:
                lowest_card_value = player_lowest_card
                lowest_card_player = player.name
        return lowest_card_player
    
    def update_ui(self):
        self.ai_show_hand(self.ai_player, self.ai_hand_frame)
        self.player_show_hand(self.human_player, self.hand_frame)
    def player_show_hand(self, player, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Display the player's hand
        for i, card in enumerate(player.hand):
            image = Image.open(card.image_path)
            image = image.resize((60, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            card_button = tk.Button(frame, image=photo, command=lambda c=card: self.toggle_card_selection(c))
            card_button.image = photo  # Prevent garbage collection
            card_button.grid(row=0, column=i)
    def ai_show_hand(self, player, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Show the back of the card for the AI's hand
        for i in range(len(player.hand)):
            image = Image.open('cards/card_back.png')  # Ensure this path is correct
            image = image.resize((60, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            card_label = tk.Label(frame, image=photo)
            card_label.image = photo  # Keep reference to avoid garbage collection
            card_label.grid(row=0, column=i)    
    def toggle_card_selection(self, card):
        if card in self.selected_cards:
            self.selected_cards.remove(card)  # Remove card from selection
        else:
            self.selected_cards.append(card)  # Add card to selection

        # Enable play button if there are selected cards
        if self.selected_cards:
            self.play_button.config(state=tk.NORMAL)
        else:
            self.play_button.config(state=tk.DISABLED)
    def play_card(self):
        if self.selected_cards:
            self.table.played_cards.clear()
            for card in self.selected_cards:
                self.table.place_card(self.human_player, card)
            messagebox.showinfo("Played Card", f"You played: {', '.join(map(str, self.selected_cards))}")
            self.selected_cards.clear()  # Clear selected cards
            self.update_ui()
            self.update_played_cards()

            # AI plays immediately after the human
    
            self.ai_play(self.table.played_cards)  
            self.check_game_over()
    def human_pass_card(self):
        self.ai_play(self.table.played_cards)
        self.update_ui()
        self.update_played_cards()
    def ai_pass_card(self):
        self.update_ui()
        self.update_played_cards()

    def ai_play(self):
        played_card = self.ai_player.make_move()

        if played_card:
            print("played_card:", played_card)
            self.table.place_card(self.ai_player, played_card)
            messagebox.showinfo("AI Played Card", f"AI played: {played_card}")
            self.update_ui()
            self.update_played_cards()  # Update the displayed played cards
            self.check_game_over()
    def check_game_over(self):
        if not self.human_player.hand:
            messagebox.showinfo("Game Over", "You have no cards left! AI wins!")
            self.root.quit()
        elif not self.ai_player.hand:
            messagebox.showinfo("Game Over", "AI has no cards left! You win!")
            self.root.quit()

    def update_played_cards(self):
        # Clear the frame before displaying new cards
        for widget in self.played_cards_frame.winfo_children():
            widget.destroy()

        for i, card in enumerate(self.table.played_cards):
            # Load card image
            image = Image.open(card.image_path)
            image = image.resize((60, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            # Display card image in the UI
            card_label = tk.Label(self.played_cards_frame, image=photo)
            card_label.image = photo  # Prevent garbage collection
            card_label.grid(row=0, column=i)
           
if __name__ == "__main__":
    root = tk.Tk()
    game = ThirteenGameGUI(root)
    root.mainloop()