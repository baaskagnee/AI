import tkinter as tk
from tkinter import messagebox, Canvas
import random
from PIL import Image, ImageTk  # Pillow-г импортлох

# Картуудын утга болон өнгийг тодорхойлох   
SUITS = ['diamonds', 'clubs','hearts' , 'spades']
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
    
    def sort_hand(self):
        self.hand.sort(key=lambda card: (VALUES.index(card.value), SUITS.index(card.suit)))

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
                card_value_index = VALUES.index(first_card.value)

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
            Player('Машин', hands[1])  # Хоёрдугаар тоглогчийн нэрийг "Машин" гэж тохируулах
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


        else:
            # If cards have been played, enforce higher card requirement
            if len(self.selected_cards) == len(self.table.played_cards):
                # Compare only if the number of selected cards matches played cards
                if all(self.selected_cards[i].value > self.table.played_cards[i].value for i in range(len(self.selected_cards))):
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