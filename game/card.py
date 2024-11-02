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
class CardMan:
    def __init__(self, name, hand):
        self.name = name  # Player's name
        self.hand = hand  # Player's hand (list of Card objects)
        self.opponent_hand = []  # List to store opponent's played cards

class CardManAI(CardMan):
    def __init__(self, name, hand):
        super().__init__(name, hand)

    def play_turn(self, opponent_played_cards):
        # If the opponent has played 5 cards, try to play the best possible hand
        if opponent_played_cards and len(opponent_played_cards) == 5:
            best_sequence = self.find_best_sequence()
            if best_sequence:
                return best_sequence
        
        # If not, play strategically based on opponent's last card
        if opponent_played_cards:
            opponent_card_value = VALUES[opponent_played_cards[0].value]
            higher_cards = [card for card in self.hand if VALUES[card.value] > opponent_card_value]

            if higher_cards:
                # Play the lowest of the higher cards to minimize loss
                best_card = min(higher_cards, key=lambda card: VALUES[card.value])
                self.hand.remove(best_card)
                return [best_card]

        # If no valid plays, pass or play a low card
        if len(self.hand) <= len(self.opponent_hand):
            return self.pass_turn()  # Option to pass
        else:
            # Randomly choose to either play the lowest card or a random card
            if random.choice([True, False]):
                lowest_card = min(self.hand, key=lambda card: VALUES[card.value])
                self.hand.remove(lowest_card)
                return [lowest_card]
            else:
                # Play a random card
                card_to_play = random.choice(self.hand)
                self.hand.remove(card_to_play)
                return [card_to_play]

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


# Table class for managing player hands and played cards
class Table:
    def __init__(self, players):
        self.players = players  # List of players at the table
        self.played_cards = []  # Cards played on the table

    def place_card(self, player, card):
        """Places a card from a player's hand on the table without clearing previous plays."""
        if card in player.hand:
            player.play_card(card)
            self.played_cards.append(card)
        else:
            print(f"Card {card} not found in {player.name}'s hand.")

    def start_new_round(self):
        """Clears played cards at the beginning of a new round."""
        self.played_cards.clear()



    def show_played_cards(self):
        """Shows the cards played on the table."""
        if not self.played_cards:
            return "No cards have been played yet."
        return ', '.join(map(str, self.played_cards))

    def reset_table(self):
        """Clears the played cards from the table."""
        self.played_cards.clear()

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

        self.pass_button = tk.Button(root, text="Pass", command=self.pass_card)
        self.pass_button.pack(pady=10)

        self.selected_card_label = tk.Label(root, text="")
        self.selected_card_label.pack(pady=10)

        self.selected_cards = []  # Сонгосон картуудын жагсаалт
        self.deck = Deck()
        self.players = []

    def find_lowest_card_player(self):
        lowest_card_player = None
        lowest_card_value = None

        for player in self.players:
            # Хэрвээ тоглогчийн гарт карт байгаа бол
            if player.hand:
                # Эхний картын утгыг аваад
                first_card = player.hand[0]
                card_value_index = VALUES[first_card.value]


                # Хэрвээ энэ нь хамгийн бага утга байвал
                if lowest_card_value is None or card_value_index < lowest_card_value:
                    lowest_card_value = card_value_index
                    lowest_card_player = player.name

        return lowest_card_player
    

    def start_game(self):
        self.start_button.config(state=tk.DISABLED)
        hands = self.deck.deal()
        self.players = [
            Player('Хүн', hands[0]),  # Нэгдүгээр тоглогчийн нэрийг "Хүн" гэж тохируулах
            Player('Cardman', hands[1])  # Хоёрдугаар тоглогчийн нэрийг "Машин" гэж тохируулах
        ]

        for player in self.players:
            player.sort_hand()
        self.table = Table(self.players)  # Тоглогчдыг ашиглан ширээг инициализаци хийх
        self.current_player = 0
        self.update_ui()
        
        lowest_card_player = self.find_lowest_card_player()
        print(lowest_card_player)
        self.current_player = next(i for i, player in enumerate(self.players) if player.name == lowest_card_player)  # Эхлэх тоглогчийг тохируулах
        self.play_card()

        self.update_ui()
        print(f"Хамгийн бага хөзөртэй тоглогч: {lowest_card_player} эхэлж байна.")
        self.play_card()
    
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
    def pass_card(self):
        self.table.played_cards.clear()
        self.selected_cards.clear()
        self.current_player = (self.current_player + 1) % len(self.players)
        self.update_ui()
        self.update_played_cards()

    def play_card(self):
        player = self.players[self.current_player]

        if len(self.table.played_cards) == 0:
            # If no cards have been played, any valid move can be made
            if len(self.selected_cards) == 1:
                card = self.selected_cards[0]
                if card in player.hand:
                    self.table.place_card(player, card)
                else:
                    print("Анхаар!", "Сонгосон хөзөр тоглогчийн гарт байх ёстой.")
                    self.selected_cards.clear()
                    return  # Allow retry
            elif len(self.selected_cards) == 2:
                card1, card2 = self.selected_cards
                if card1 in player.hand and card2 in player.hand:
                    if card1.value == card2.value:
                        self.table.place_card(player, card1)
                        self.table.place_card(player, card2)
                    else:
                        print("Анхаар!", "Хоёр хөзөрийн утгууд ижил байх ёстой.")
                        self.selected_cards.clear()
                        return  # Allow retry
                else:
                    print("Анхаар!", "Сонгосон хөзрүүд тоглогчийн гарт байх ёстой.")
                    self.selected_cards.clear()
                    return  # Allow retry
            elif len(self.selected_cards) == 3:
                card1, card2, card3 = self.selected_cards
                
                # Check if all selected cards are in the player's hand
                if card1 in player.hand and card2 in player.hand and card3 in player.hand:
                    self.table.played_cards.clear()  # Clear previously played cards
                    
                    # Check if all three cards have the same value
                    if card1.value == card2.value == card3.value:
                        # Place the cards on the table
                        self.table.place_card(player, card1)
                        self.table.place_card(player, card2)
                        self.table.place_card(player, card3)
                    else:
                        print("Анхаар!", "Гурван хөзөрийн утгууд ижил байх ёстой.")  # Warning: All three card values must be the same
                        self.selected_cards.clear()
                        return  # Allow retry
            elif len(self.selected_cards) == 5:
                validator = FiveCardValidator(self.selected_cards)
                if validator.is_same_suit():
                    print("is_same_suit")
                    for card in self.selected_cards:
                        self.table.place_card(player, card)
                    self.selected_cards.clear()
                    self.selected_card_label.config(text="5 cards played.")
                elif validator.is_sequence():
                    print("is_sequence")
                    for card in self.selected_cards:
                        self.table.place_card(player, card)
                    self.selected_cards.clear()
                    self.selected_card_label.config(text="5 cards played.")
                elif validator.is_poker():
                    print("is_poker")
                    for card in self.selected_cards:
                        self.table.place_card(player, card)
                    self.selected_cards.clear()
                    self.selected_card_label.config(text="5 cards played.")   
                elif validator.is_fullHouse():
                    print("is_fullHouse")
                    for card in self.selected_cards:
                        self.table.place_card(player, card)
                    self.selected_cards.clear()
                    self.selected_card_label.config(text="5 cards played.")      
                elif validator.is_straightFlush():
                    print("is_straightFlush")
                    for card in self.selected_cards:
                        self.table.place_card(player, card)
                    self.selected_cards.clear()
                    self.selected_card_label.config(text="5 cards played.")          
                else:
                    self.selected_card_label.config(text="5 cards must be a consecutive sequence and same suit.")
                    self.selected_cards.clear()
                    return

# Assuming self.selected_cards and self.table.played_cards are defined somewhere in your class
        elif len(self.selected_cards) == len(self.table.played_cards) == 5:
            # Create validators for the played cards and the selected cards
            played_validator = FiveCardValidator(self.table.played_cards)
            selected_validator = FiveCardValidator(self.selected_cards)
            
            played_strength = played_validator.evaluate_hand()
            selected_strength = selected_validator.evaluate_hand() 

            # Compare strengths of the hands
            if played_strength < selected_strength:
                for card in self.selected_cards:
                    self.table.place_card(player, card)
                self.selected_cards.clear()  # Clear selected cards after playing them
                self.selected_card_label.config(text="5 cards played.")
            elif played_strength == selected_strength:
        # Compare the highest cards in both hands
                played_high_card = max(self.table.played_cards, key=lambda card: VALUES[card.value])
                selected_high_card = max(self.selected_cards, key=lambda card: VALUES[card.value])

                if VALUES[played_high_card.value] < VALUES[selected_high_card.value]:
                    for card in self.selected_cards:
                        self.table.place_card(player, card)
                    self.selected_cards.clear()
                    self.selected_card_label.config(text="5 cards played, with a higher card!")

            else:
                self.selected_card_label.config(text="Selected cards do not beat the played cards.")

                        
        elif len(self.selected_cards) == len(self.table.played_cards):
            # Compare only if the number of selected cards matches played cards
            if all(VALUES[self.selected_cards[i].value] > VALUES[self.table.played_cards[i].value] for i in range(len(self.selected_cards))):

                if len(self.selected_cards) == 1:
                    card = self.selected_cards[0]
                    if card in player.hand:
                        self.table.played_cards.clear()
                        self.table.place_card(player, card)
                    else:
                        print("Анхаар!", "Сонгосон хөзөр тоглогчийн гарт байх ёстой.")
                        self.selected_cards.clear()
                        return  # Allow retry
                elif len(self.selected_cards) == 2:
                    card1, card2 = self.selected_cards
                    if card1 in player.hand and card2 in player.hand:
                        self.table.played_cards.clear()
                        if card1.value == card2.value:
                            self.table.place_card(player, card1)
                            self.table.place_card(player, card2)
                            
                        else:
                            print("Анхаар!", "Хоёр хөзөрийн утгууд ижил байх ёстой.")
                            self.selected_cards.clear()
                            return  # Allow retry
                    else:
                        print("Анхаар!", "Сонгосон хөзрүүд тоглогчийн гарт байх ёстой.")
                        self.selected_cards.clear()
                        return  # Allow retry
                elif len(self.selected_cards) == 3:
                    card1, card2, card3 = self.selected_cards
                    
                    # Check if all selected cards are in the player's hand
                    if card1 in player.hand and card2 in player.hand and card3 in player.hand:
                        self.table.played_cards.clear()  # Clear previously played cards
                        
                        # Check if all three cards have the same value
                        if card1.value == card2.value == card3.value:
                            # Place the cards on the table
                            self.table.place_card(player, card1)
                            self.table.place_card(player, card2)
                            self.table.place_card(player, card3)
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
            elif all(VALUES[self.selected_cards[i].value] == VALUES[self.table.played_cards[i].value] for i in range(len(self.selected_cards))):

                if all(SUITS[self.selected_cards[i].suit] > SUITS[self.table.played_cards[i].suit] for i in range(len(self.selected_cards))):

                    if len(self.selected_cards) == 1:
                        card = self.selected_cards[0]
                        if card in player.hand:
                            self.table.played_cards.clear()
                            self.table.place_card(player, card)
                        else:
                            print("Анхаар!", "Сонгосон хөзөр тоглогчийн гарт байх ёстой.")
                            self.selected_cards.clear()
                            return  # Allow retry
                    elif len(self.selected_cards) == 2:
                        card1, card2 = self.selected_cards
                        if card1 in player.hand and card2 in player.hand:
                            self.table.played_cards.clear()
                            if card1.value == card2.value:
                                self.table.place_card(player, card1)
                                self.table.place_card(player, card2)
                                
                            else:
                                print("Анхаар!", "Хоёр хөзөрийн утгууд ижил байх ёстой.")
                                self.selected_cards.clear()
                                return  # Allow retry
                        else:
                            print("Анхаар!", "Сонгосон хөзрүүд тоглогчийн гарт байх ёстой.")
                            self.selected_cards.clear()
                            return  # Allow retry
                    elif len(self.selected_cards) == 3:
                        card1, card2, card3 = self.selected_cards
                        
                        # Check if all selected cards are in the player's hand
                        if card1 in player.hand and card2 in player.hand and card3 in player.hand:
                            self.table.played_cards.clear()  # Clear previously played cards
                            
                            # Check if all three cards have the same value
                            if card1.value == card2.value == card3.value:
                                # Place the cards on the table
                                self.table.place_card(player, card1)
                                self.table.place_card(player, card2)
                                self.table.place_card(player, card3)
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
                else:
                    print("Анхаар!", "Таны сонгосон хөзөр өмнөхөөсөө өндөр утгатай байх ёстой.")
                    return
            else:
                print("тоглох хөзрийн тоо таарахгүй байна")
                return
        else:
            print("тоглох хөзрийн тоо таарахгүй байна")
            return

        # Update the UI after a successful play
        if len(self.players[self.current_player].hand) == 0:  # Accessing the player's hand correctly
            print("game over")
        else:
            self.selected_card_label.config(text=f"Played: {', '.join(map(str, self.selected_cards))}")
            self.selected_cards.clear()
            self.play_button.config(state=tk.DISABLED)
            self.current_player = (self.current_player + 1) % len(self.players)
            self.update_ui()
            self.update_played_cards()


    def toggle_card_selection(self, card):
        if card in self.selected_cards:
            self.selected_cards.remove(card)  # Хэрэв карт жагсаалтад байгаа бол устгана
        else:
            self.selected_cards.append(card)  # Шинээр карт сонгох үед жагсаалтад нэмнэ

        # Сонгосон картуудын жагсаалтыг харуулах
        self.selected_card_label.config(text=f"Selected: {', '.join(map(str, self.selected_cards))}")

        # Хэрэв сонгосон картууд 1 эсвэл 2 байгаа бол Play товчийг идэвхжүүлнэ
        if len(self.selected_cards) in (1, 2, 3, 5):
            self.play_button.config(state=tk.NORMAL)
        else:
            self.play_button.config(state=tk.DISABLED)


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