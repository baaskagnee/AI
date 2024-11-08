# Ajillad baiga gui
import tkinter as tk
from tkinter import messagebox, Button,PhotoImage,Label
import random
from PIL import Image, ImageTk
from collections import defaultdict
from itertools import combinations

# Define card values and suits
SUITS = {
    'diamonds': 1,
    'clubs': 2,
    'hearts': 3,
    'spades': 4
}
SUIT_RANKS = {
    'spades': 4,
    'hearts': 3,
    'diamonds': 2,
    'clubs': 1
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
def bttn(parent, x, y, image_path, hover_image_path, command):
    # Load images
    try:
        default_image = Image.open(image_path)
        default_photo = ImageTk.PhotoImage(default_image)   
        hover_image = Image.open(hover_image_path)
        hover_photo = ImageTk.PhotoImage(hover_image)
    except Exception as e:
        print(f"Error loading button images: {e}")
        return

    button = Button(parent, image=default_photo, command=command, borderwidth=0)
    button.image = default_photo  # Keep a reference to avoid garbage collection
    button.place(x=x, y=y)

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
class FiveCardValidator:
    def __init__(self, cards):
        self.cards = cards

    def is_sequence(self):
        values = sorted([VALUES[card.value] for card in self.cards])
        return all(values[i] + 1 == values[i + 1] for i in range(len(values) - 1))

    def is_same_suit(self):
        return all(card.suit == self.cards[0].suit for card in self.cards)

    def is_poker(self):
        value_counts = {}
        for card in self.cards:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1
        return 4 in value_counts.values()

    def is_fullHouse(self):
        value_counts = {}
        for card in self.cards:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1
        counts = list(value_counts.values())
        return sorted(counts) == [2, 3]

    def is_straightFlush(self):
        return self.is_sequence() and self.is_same_suit()

    def evaluate_hand(self):
        if self.is_straightFlush():
            return 8  # Highest hand: Straight Flush
        elif self.is_poker():
            return 7  # Four of a Kind
        elif self.is_fullHouse():
            return 6  # Full House
        elif self.is_same_suit():
            return 5  # Flush
        elif self.is_sequence():
            return 4  # Straight
        elif self.is_three_of_a_kind():
            return 3  # Three of a Kind
        elif self.is_two_pair():
            return 2  # Two Pair
        elif self.is_one_pair():
            return 1  # One Pair
        else:
            return 0  # High Card

    def is_three_of_a_kind(self):
        value_counts = {}
        for card in self.cards:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1
        return 3 in value_counts.values() and len(value_counts) > 2

    def is_two_pair(self):
        value_counts = {}
        for card in self.cards:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1
        return list(value_counts.values()).count(2) == 2

    def is_one_pair(self):
        value_counts = {}
        for card in self.cards:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1
        return 2 in value_counts.values()
class AICardManager(Player):
    def __init__(self, name, hand):
        super().__init__(name, hand)

    def make_move(self, played_cards):
        print("тоглогчийн тоглосон хөзрийн тоо:", len(played_cards))
        """Тоглогдсон хөзрөөс илүү утгатай хөзрийг сонгож буцаана."""
        # Тоглогдсон хөзрийн хамгийн том утгыг олно
        if len(played_cards) == 1:
            print("тоглогч 1 хөзрөөр тоглосон")
            if played_cards:
                max_played_value = max(VALUES[card.value] for card in played_cards)
                # Тоглогдсон хөзрөөс илүү утгатай хөзрүүдийн жагсаалт үүсгэнэ
                higher_cards = [card for card in self.hand if VALUES[card.value] > max_played_value]
                # Илүү утгатай хөзөр байвал хамгийн бага утгатайг нь сонгож тоглоно
                if higher_cards:
                    best_card = min(higher_cards, key=lambda card: VALUES[card.value])
                    return best_card
                else:
                    # Илүү утгатай хөзөр байхгүй бол дамжуулна
                    return "pass"
        elif len(played_cards) == 0:  # When it's the first move
            print("no cards played yet")
            
            # Check if AI has a five-card combo
            five_card_combo = self.play_best_five_card_combo([])
            if five_card_combo:
                print("AI тоглогч 5 хөзрийн хослол тоглов.")
                return five_card_combo
            
            # If no five-card combo, check if AI has a triple
            triple = self.play_best_triple([])
            if triple:
                print("AI тоглогч гурвалсан хослол тоглов.")
                return triple
            
            # If no triple, check if AI has a pair
            pair = self.play_best_pair([])
            if pair:
                print("AI тоглогч хос хөзөр тоглов.")
                return pair
            
            # If no combinations, play the highest single card
            highest_card = max(self.hand, key=lambda card: VALUES[card.value])
            print("AI тоглогч хамгийн өндөр хөзрийг тоглов.")
            return highest_card
        elif len(played_cards) == 2:
            # Нөгөө тоглогчийн хос хөзрийн эсрэг хамгийн өндөр хосыг тоглохыг оролд
            best_pair = self.play_best_pair(played_cards)
            if best_pair:
                print(f"AI тоглогч тоглох хослол: {best_pair}")
                return best_pair  # Хос хөзрийг буцаана
            else:
                print("AI тоглогч дамжууллаа.")
                return "pass"  # Тоглох боломжгүй бол дамжуулна
                # Дамжуулах
        elif len(played_cards) == 3:
            card_triple = self.play_best_triple(played_cards)
            if card_triple:
                print(f"AI тоглогч тоглох гурвалсан хослол: {card_triple}")
            else:
                print("AI тоглогч тоглох боломжгүй байна.")
                return "pass"
        elif len(played_cards) == 5:  # Нөгөө тоглогчийн 5 хөзрөөр тоглосон эсэхийг шалгана
            card_combo = self.play_best_five_card_combo(played_cards)
            if card_combo:
                print(f"AI тоглогч тоглох 5 хөзрийн хослол: {card_combo}")
            else:
                print("AI тоглогч тоглох боломжгүй байна.")
                return None

    def play_best_pair(self, last_played_pair):
        """AI chooses the best pair to play against the opponent's pair."""
        # Collect pairs in hand
        pairs = self.find_multiples(2)

        if last_played_pair:
            # Evaluate the last played pair's value
            last_pair_value = VALUES[last_played_pair[0].value]
            
            # Find the first stronger pair to play
            for pair in pairs:
                if VALUES[pair[0].value] > last_pair_value:
                    return pair  # Play this pair if it's stronger
            
            return None  # No pair strong enough to play

        elif last_played_pair == []:
            # If no pair has been played yet, play the strongest pair
            return pairs[0] if pairs else None  # Return strongest pair or None if no pairs

    def find_multiples(self, count):
        """Гарт байгаа тодорхой тооны ижил утгатай хөзрүүдийн бүлгийг хайж буцаана."""
        multiples = []
        value_counts = {}
        # Гарт байгаа хөзрүүдийн утгыг тоолох
        for card in self.hand:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1
        # Тухайн утгатай хөзрүүдийн тоо 'count'-ээс их буюу тэнцүү бол бүлэгт нэмэх
        for value, cnt in value_counts.items():
            if cnt >= count:
                same_value_cards = [card for card in self.hand if card.value == value]
                multiples.append(same_value_cards[:count])  # Зөвхөн 'count' тооны хөзрийг бүлэг болгон авах

        return multiples

    def play_best_triple(self, last_played_triple):
        """AI chooses the best triple (three of a kind) to play against the opponent's triple, or plays any triple if it's the first move."""
        # Collect triples in hand
        triples = self.find_multiples(3)
        
        # If no triples are available, return None
        if not triples:
            return None
        
        # Check if there was a previously played triple
        if last_played_triple:
            # Evaluate the last played triple's value
            last_triple_value = VALUES[last_played_triple[0].value]
            
            # Find the first stronger triple to play
            for triple in triples:
                if VALUES[triple[0].value] > last_triple_value:

                    return triple  # Play this stronger triple
        else:
            # If no triple was previously played, play the lowest triple to use up cards
            lowest_triple = min(triples, key=lambda triple: VALUES[triple[0].value])
            return lowest_triple  # Play the lowest triple available

        return   # No triple strong enough to play if none met the requirements


    def play_best_five_card_combo(self, last_played_combo):
        """AI хамгийн тохиромжтой 5 хөзрийн хослолыг тоглоно."""
        combo_to_play = self.choose_five_card_combo(last_played_combo)
        if combo_to_play:
            for card in combo_to_play:
                self.play_card(card)
            return combo_to_play
        else:
            return None  # Тоглох боломжгүй бол ямар ч хослолыг тоглохгүй
        
    def choose_five_card_combo(self, last_played_combo):
        """AI selects a five-card combo that can beat the opponent's last played combo."""
        if len(self.hand) < 5:
            return None  # No combo available if fewer than 5 cards in hand.

        # Sort hand and find all five-card combos
        self.sort_hand()
        possible_combos = self.find_five_card_combos()

        # If no combo has been played by the opponent, play the strongest combo
        if not last_played_combo:
            return possible_combos[0] if possible_combos else None

        # Find the first combo that is stronger than the last played combo
        for combo in possible_combos:
            if self.is_stronger_combo(combo, last_played_combo):
                return combo  # Play this combo if it’s stronger

        return None  # No stronger combo found

    
    def is_stronger_combo(self, combo, other_combo):
        """5 хөзрийн хослолыг харьцуулж хүчтэй эсэхийг тодорхойлно."""
        combo_value = self.evaluate_combo(combo)
        other_combo_value = self.evaluate_combo(other_combo)
        
        return combo_value > other_combo_value

    def evaluate_combo(self, combo):
        """Хослолын үнэлгээг тодорхойлно."""
        validator = FiveCardValidator(combo)
        return validator.evaluate_hand()


    def find_five_card_combos(self):
        """AI-ийн гар дахь боломжит 5 хөзрийн хослолуудыг илүү хурдан олно."""
        combos = []
        
        # 5 картын бүх боломжит хослолыг шалгаж, хүчтэй хослолыг олно
        for combo in combinations(self.hand, 5):
            validator = FiveCardValidator(combo)
            if validator.evaluate_hand() > 0:  # Хэрэв хослолын үнэлгээ 0-ээс их байвал хүчтэй хослол байна
                combos.append(combo)
        
        return combos

class Table:
    def __init__(self, players):
        self.players = players  # List of players at the table
        self.played_cards = []  # Cards played on the table

    def place_card(self, player, cards):
        """Place a card or a list of cards from the player's hand on the table."""
        # Check if cards is a list (could also handle single card input)
        if isinstance(cards, list) and cards:  # Ensure cards is a non-empty list
            for card in cards:  # Loop through each card in the list
                if card in player.hand:  # Check if the card is in the player's hand
                    player.play_card(card)
                    self.played_cards.append(card)
                    print(f"Card {card} added to the table.")
                else:
                    print(f"Card {card} not found in {player.name}'s hand.")
        elif cards:  # If a single card was passed, convert to list and process
            if cards in player.hand:
                player.play_card(cards)
                self.played_cards.append(cards)
                print(f"Card {cards} added to the table.")
            else:
                print(f"Card {cards} not found in {player.name}'s hand.")
        else:
            print("No valid cards to play.")



    def start_new_round(self):
        """Start a new round by clearing the played cards."""
        self.played_cards.clear()

    def show_played_cards(self):
        """Display the cards played on the table."""
        if not self.played_cards:
            return "No cards have been played yet."
        return ', '.join(map(str, self.played_cards))

class CardGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Card Game")
        self.root.geometry("1000x800")
        # Store the PhotoImage object as an instance variable
        image = Image.open("assets/table.png")
        resized_image = image.resize((1000, 800), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(resized_image)

        # Set the resized image as background
        self.my_label = tk.Label(root, image=self.bg)
        self.my_label.place(x=0, y=0, relheight=1, relwidth=1)

        # UI Components
        self.player_label = tk.Label(root, text="13CARD GAME")
        self.player_label.pack(pady=50)

        self.ai_label = tk.Label(root, text="AI's Hand")
        self.ai_label.pack()
        self.ai_hand_frame = tk.Frame(root)
        self.ai_hand_frame.pack(pady=10)

        self.played_cards_frame = tk.Frame(root)
        self.played_cards_frame.pack(pady=20)

        self.player_hand_label = tk.Label(root, text="Your Hand")
        self.player_hand_label.place(y=600,x=480)
        self.hand_frame = tk.Frame(root)
        self.hand_frame.place(y=480,x=150)

        play_card =  PhotoImage(file='assets/play_card.png')
        self.play_button = tk.Button(root, text="Play Card", command=self.play_card, state=tk.DISABLED)
        self.play_button.place(y=700,x=350)
        # bttn(root,850, 400, 'assets/play_card.png','assets/play_card_hover.png',lambda: self.play_card)

        self.pass_button = tk.Button(root, text="Pass", command=self.pass_card)
        self.pass_button.place(y=700,x=600)
        # Create a deck and deal cards to players
        self.deck = Deck()
        hands = self.deck.deal()

        self.human_player = Player("Human", hands[0])
        self.human_player.sort_hand()
        self.ai_player = AICardManager("AI", hands[1])
        self.players = [self.human_player, self.ai_player]
        self.table = Table(self.players)

        print(self.ai_player.show_hand())

        self.selected_cards = []  # Store selected cards
        self.update_ui()

    def update_ui(self):
        player = self.players[0]
        ai = self.players[1]
        self.ai_show_hand(ai, self.ai_hand_frame)
        self.player_show_hand(player, self.hand_frame)

    def player_show_hand(self, player, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Display the player's hand
        for i, card in enumerate(player.hand):
            image = Image.open(card.image_path)
            image = image.resize((50, 80), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            card_button = tk.Button(frame, image=photo, command=lambda c=card: self.toggle_card_selection(c))
            card_button.image = photo  # Prevent garbage collection
            card_button.grid(row=5, column=i)

    def ai_show_hand(self, player, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Show the back of the card for the opponent
        for i in range(len(player.hand)):
            image = Image.open('cards/card_back.png')
            image = image.resize((50, 80), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            card_label = tk.Label(frame, image=photo)
            card_label.image = photo  # Prevent garbage collection
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

    def pass_card(self):
        self.table.played_cards.clear()
        self.ai_play(self.table.played_cards)
        self.update_ui()
        self.update_played_cards()

    def play_card(self):
        if len(self.table.played_cards)==0:
            if len(self.selected_cards)==1:
                card = self.selected_cards[0]
                if card in self.human_player.hand:
                    self.table.place_card(self.human_player, card)

                else:
                    print("Анхаар!", "Сонгосон хөзөр тоглогчийн гарт байх ёстой.")
                    self.selected_cards.clear()
                    return  # Allow retry                    
            elif len(self.selected_cards) == 2:
                card = [None, None]  # Initialize a list with two slots
                card[0], card[1] = self.selected_cards

                # Check if both selected cards are in the player's hand
                if card[0] in self.human_player.hand and card[1] in self.human_player.hand:
                    # Check if both cards have the same value
                    if card[0].value == card[1].value:
                        self.table.place_card(self.human_player, card)
                                # messagebox.showinfo("Played Card", f"You played: {', '.join(map(str, self.selected_cards))}")


                    else:
                        print("Анхаар!", "Хоёр хөзөрийн утгууд ижил байх ёстой.")
                        self.selected_cards.clear()
            elif len(self.selected_cards) == 3:
                card = [None, None, None]  
                card[0], card[1], card[2]= self.selected_cards
                if card[0] in self.human_player.hand and card[1] in self.human_player.hand and card[2] in self.human_player.hand:
                    if card[0].value == card[1].value == card[2].value:
                        self.table.place_card(self.human_player, card)

                    else:
                        print("Анхаар!", "Хоёр хөзөрийн утгууд ижил байх ёстой.")
                        self.selected_cards.clear()
            elif len(self.selected_cards) == 5:

                validator = FiveCardValidator(self.selected_cards)
                if validator.is_same_suit():
                    self.table.played_cards.clear()
                    print("is_same_suit")
                    for card in self.selected_cards:
                        self.table.place_card(self.human_player, card)
                    self.selected_cards.clear()
                    #self.selected_card_label.config(text="5 cards played.")
                elif validator.is_sequence():
                    print("is_sequence")
                    self.table.played_cards.clear()
                    for card in self.selected_cards:
                        self.table.place_card(self.human_player, card)
                    self.selected_cards.clear()
                    # self.selected_card_label.config(text="5 cards played.")
                elif validator.is_poker():
                    print("is_poker")
                    self.table.played_cards.clear()
                    for card in self.selected_cards:
                        self.table.place_card(self.human_player, card)
                    self.selected_cards.clear()
                    # self.selected_card_label.config(text="5 cards played.")   
                elif validator.is_fullHouse():
                    print("is_fullHouse")
                    self.table.played_cards.clear()
                    for card in self.selected_cards:
                        self.table.place_card(self.human_player, card)
                    self.selected_cards.clear()
                    # self.selected_card_label.config(text="5 cards played.")      
                elif validator.is_straightFlush():
                    print("is_straightFlush")
                    self.table.played_cards.clear()
                    for card in self.selected_cards:
                        self.table.place_card(self.human_player, card)
                    self.selected_cards.clear()
                    # self.selected_card_label.config(text="5 cards played.")          
                else:
                    # self.selected_card_label.config(text="5 cards must be a consecutive sequence and same suit.")
                    print("Тоглох боломжгүй байна")
                    self.selected_cards.clear()
                    return               
        elif len(self.selected_cards) == len(self.table.played_cards) == 5:          
            # Create validators for the played cards and the selected cards
            played_validator = FiveCardValidator(self.table.played_cards)
            selected_validator = FiveCardValidator(self.selected_cards)
            
            played_strength = played_validator.evaluate_hand()
            selected_strength = selected_validator.evaluate_hand() 

            # Compare strengths of the hands
            if played_strength < selected_strength:
                self.table.played_cards.clear()
                for card in self.selected_cards:
                    self.table.place_card(self.human_player, card)
                self.selected_cards.clear()  # Clear selected cards after playing them
                self.selected_card_label.config(text="5 cards played.")
            elif played_strength == selected_strength:
        # Compare the highest cards in both hands
                played_high_card = max(self.table.played_cards, key=lambda card: VALUES[card.value])
                selected_high_card = max(self.selected_cards, key=lambda card: VALUES[card.value])

                if VALUES[played_high_card.value] < VALUES[selected_high_card.value]:
                    self.table.played_cards.clear()
                    for card in self.selected_cards:
                        self.table.place_card(self.human_player, card)
                    self.selected_cards.clear()
                    self.selected_card_label.config(text="5 cards played, with a higher card!")

            else:
                self.selected_card_label.config(text="Selected cards do not beat the played cards.")

        elif len(self.selected_cards) == len(self.table.played_cards):
            # Compare only if the number of selected cards matches played cards
            # if all(VALUES[self.selected_cards[i].value] == VALUES[self.table.played_cards[i].value] for i in range(len(self.selected_cards))) and all(VALUES[self.selected_cards[i].suit] > VALUES[self.table.played_cards[i].suit] for i in range(len(self.selected_cards))):
            #if (all(VALUES[self.selected_cards[i].value] > VALUES[self.table.played_cards[i].value] for i in range(len(self.selected_cards))) or (all(VALUES[self.selected_cards[i].value] == VALUES[self.table.played_cards[i].value] for i in range(len(self.selected_cards))) and all(VALUES[self.selected_cards[i].suit] > VALUES[self.table.played_cards[i].suit] for i in range(len(self.selected_cards))))):
            if (all(VALUES[self.selected_cards[i].value] > VALUES[self.table.played_cards[i].value] for i in range(len(self.selected_cards)))or (all(VALUES[self.selected_cards[i].value] == VALUES[self.table.played_cards[i].value] for i in range(len(self.selected_cards)))and all(SUIT_RANKS[self.selected_cards[i].suit] > SUIT_RANKS[self.table.played_cards[i].suit] for i in range(len(self.selected_cards))))):

                if len(self.selected_cards) == 1:
                    card = self.selected_cards[0]
                    if card in self.human_player.hand:
                        self.table.played_cards.clear()
                        self.table.place_card(self.human_player, card)
                    else:
                        print("Анхаар!", "Сонгосон хөзөр тоглогчийн гарт байх ёстой.")
                        self.selected_cards.clear()
                        return  # Allow retry
                elif len(self.selected_cards) == 2:
                    card = [None, None]  # Initialize a list with two slots
                    card[0], card[1] = self.selected_cards

                # Check if both selected cards are in the player's hand
                    if card[0] in self.human_player.hand and card[1] in self.human_player.hand:
                    # Check if both cards have the same value
                        if card[0].value == card[1].value:
                            self.table.played_cards.clear()
                            self.table.place_card(self.human_player, card)
                                # messagebox.showinfo("Played Card", f"You played: {', '.join(map(str, self.selected_cards))}")
                            self.selected_cards.clear()  # Clear selected cards
                            
                        else:
                            print("Анхаар!", "Хоёр хөзөрийн утгууд ижил байх ёстой.")
                            self.selected_cards.clear()
                            return  # Allow retry
                    else:
                        print("Анхаар!", "Сонгосон хөзрүүд тоглогчийн гарт байх ёстой.")
                        self.selected_cards.clear()
                        return  # Allow retry
                elif len(self.selected_cards) == 3:
                    card = [None, None, None]
                    card[0], card[1], card[2] = self.selected_cards
                    
                    # Check if all selected cards are in the player's hand
                    if card[0] in self.human_player.hand and card[1] in self.human_player.hand and card[2] in self.human_player.hand:
                        # Check if all three cards have the same value
                        if card[0].value == card[1].value == card[2].value:
                            self.table.played_cards.clear()
                            # Place the cards on the table
                            self.table.place_card(self.human_player, card)
                        else:
                            print("Анхаар!", "Гурван хөзөрийн утгууд ижил байх ёстой.")  # Warning: All three card values must be the same
                            self.selected_cards.clear()
                            return  # Allow retry
                    else:
                        print("Анхаар!", "Сонгосон хөзрүүд тоглогчийн гарт байх ёстой.")  # Warning: Selected cards must be in player's hand
                        self.selected_cards.clear()
                        return  # Allow retry
                else:
                    print("Анхаар!", "Таны сонгосон хөзөр өмнөхөөсөө өндөр утгатай байх ёстой.")  # Warning: Selected cards must be higher than the previous ones
                    self.selected_cards.clear()
                    return  # Allow retry
            
            else:
                print("тоглох хөзөр өмнөхөөсөө илүү байх ёстой")
                return
        else:
            print("тоглох хөзрийн тоо таарахгүй байна")
            return
        self.selected_cards.clear()  # Clear selected cards
        self.update_ui()
        self.update_played_cards()

        # AI plays immediately after the human
        print(f"AI's hand before playing: {self.ai_player.show_hand()}") 
        print("тоглогчийн тоглосон газар",self.table.played_cards)
         # Debug output
        self.check_game_over()
        self.ai_play(self.table.played_cards)
        
            # for card in self.selected_cards:
            #     self.table.place_card(self.human_player, card)
            # messagebox.showinfo("Played Card", f"You played: {', '.join(map(str, self.selected_cards))}")
            # self.selected_cards.clear()  # Clear selected cards
            # self.update_ui()
            # self.update_played_cards()

            # # AI plays immediately after the human
            # print(f"AI's hand before playing: {self.ai_player.show_hand()}")  # Debug output
            # self.ai_play(self.table.played_cards)  
            # self.check_game_over()

    def ai_play(self,played_cards):
        played_card = self.ai_player.make_move(played_cards)
        if played_card:
            self.table.played_cards.clear()
            print("played_card:", played_card)
            self.table.place_card(self.ai_player, played_card)
            messagebox.showinfo("AI Played Card", f"AI played: {played_card}")
            print("2.тоглогчийн тоглосон хөзөр:",self.table.played_cards)
            print("2.тоглогчийн тоглосон хөзрийн хэмжээ:",len(self.table.played_cards))
            self.update_ui()
            self.update_played_cards()
            self.check_game_over()
        elif not played_card:
            self.pass_card()
            print("AI passed")
        else:
            self.pass_card()
            print("AI passed")  
    
    def check_game_over(self):
        if not self.human_player.hand:
            messagebox.showinfo("Game Over", "You wins!")
            self.root.quit()
        elif not self.ai_player.hand:
            messagebox.showinfo("Game Over", "AI wins!")
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
    app = CardGameApp(root)
    root.mainloop()
