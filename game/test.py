# Ajillad baiga gui
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
        elif not played_cards:  # Хэрэв эхний тоглолт бол
            print("not played cards")
            # Хэрэв тоглогдсон хөзөр байхгүй бол хамгийн бага хөзрийг тоглоно
            lowest_card = min(self.hand, key=lambda card: VALUES[card.value])
            return lowest_card
        elif len(played_cards) == 2:
            # Хамгийн өндөр утгатай хосыг тоглох
            best_pair = self.play_best_pair(played_cards)
            if best_pair:
                print(f"AI тоглогч тоглох хослол: {best_pair}")
                return best_pair  # Хос хөзрийг буцаана
            else:
                print("AI тоглогч дамжууллаа.")
                return []  # Дамжуулах
        elif len(played_cards) == 3:
            card_triple = self.play_best_triple(played_cards)
            if card_triple:
                print(f"AI тоглогч тоглох гурвалсан хослол: {card_triple}")
            else:
                print("AI тоглогч тоглох боломжгүй байна.")
        elif len(played_cards) == 5:  # Нөгөө тоглогчийн 5 хөзрөөр тоглосон эсэхийг шалгана
            card_combo = self.play_best_five_card_combo(played_cards)
            if card_combo:
                print(f"AI тоглогч тоглох 5 хөзрийн хослол: {card_combo}")
            else:
                print("AI тоглогч тоглох боломжгүй байна.")

    def play_best_pair(self, last_played_pair):
        """AI chooses the best pair to play against the opponent's pair."""
        # Collect pairs in hand
        pairs = self.find_multiples(2)
        
        # Evaluate the last played pair's value
        last_pair_value = VALUES[last_played_pair[0].value]
        # Find the first stronger pair to play
        for pair in pairs:
            if VALUES[pair[0].value] > last_pair_value:
                return pair  # Play this pair
        
        return None  # No pair strong enough to play
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
        """AI нь нөгөө тоглогчийн тоглосон 5 хөзрийн хослолтой харьцуулах хослолыг сонгоно."""
        if len(self.hand) < 5:
            return None  # Гаранд 5-аас доош хөзөр байгаа бол хослол байхгүй.

        # Гаранд байгаа картыг эрэмбэлнэ
        self.sort_hand()

        # 5 хөзрийн хослолыг олох
        possible_combos = self.find_five_card_combos()

        # Нөгөө тоглогчийн тоглосон хослолтой харьцуулж илүү хүчтэй хослолыг олно
        for combo in possible_combos:
            if self.is_stronger_combo(combo, last_played_combo):
                return combo  # Илүү хүчтэй хослол байвал түүнийг сонгоно

        return None  # Илүү хүчтэй хослол олдохгүй бол None буцаана

    def find_five_card_combos(self):
        """AI-ийн гар дахь боломжит 5 хөзрийн хослолуудыг олно."""
        combos = []

        # AI-ийн гарын бүх 5 картын комбинацийг шалгана
        for i in range(len(self.hand)):
            for j in range(i + 1, len(self.hand)):
                for k in range(j + 1, len(self.hand)):
                    for l in range(k + 1, len(self.hand)):
                        for m in range(l + 1, len(self.hand)):
                            combo = [self.hand[i], self.hand[j], self.hand[k], self.hand[l], self.hand[m]]
                            validator = FiveCardValidator(combo)
                            if validator.evaluate_hand() > 0:
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

        self.pass_button = tk.Button(root, text="Pass", command=self.pass_card)
        self.pass_button.pack(pady=10)

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
            image = image.resize((60, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            card_button = tk.Button(frame, image=photo, command=lambda c=card: self.toggle_card_selection(c))
            card_button.image = photo  # Prevent garbage collection
            card_button.grid(row=0, column=i)

    def ai_show_hand(self, player, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Show the back of the card for the opponent
        for i in range(len(player.hand)):
            image = Image.open('cards/card_back.png')
            image = image.resize((60, 100), Image.LANCZOS)
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
                        self.table.place_card(self.human_player, card[0])
                        self.table.place_card(self.human_player, card[1])
                        self.table.place_card(self.human_player, card[2])
                        self.table.place_card(self.human_player, card[3])
                        self.table.place_card(self.human_player, card[4])
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
        print("тоглогчийн тоглосон газар",self.table.played_cards) # Debug output
        self.ai_play(self.table.played_cards)
        self.check_game_over()
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
            print("тоглогчийн тоглосон хөзөр:",self.table.played_cards)
            print("тоглогчийн тоглосон хөзрийн хэмжээ:",len(self.table.played_cards))
            self.update_ui()
            self.update_played_cards()
            self.check_game_over()
        else:
            self.pass_card()
            print("AI passed")
    
    
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
    app = CardGameApp(root)
    root.mainloop()
