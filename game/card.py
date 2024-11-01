import random

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
    
class Player:
    def __init__(self, hand):
        self.hand = hand

    def has_cards(self, required_count):
        """Тоглогчийн хөзөр нь шаардлагатай тоотой байгаа эсэхийг шалгана."""
        return len(self.hand) >= required_count

# Жишээ хэрэглээ
# Хөзрүүдийг тараасан гэж үзье
deck = Deck()
hands = deck.deal()

# Тоглогчийн экземпляр (объект) үүсгэх
player1 = Player(hands[0])
player2 = Player(hands[1])

# Тоглогчид шаардлагатай хөзрүүдийн тоог шалгах
required_count = 3  # Жишээ: 3 хөзөр шалгах
if player1.has_cards(required_count):
    print(f"Тоглогч 1-д хангалттай хөзөр байна: {required_count}")
else:
    print(f"Тоглогч 1-д хангалттай хөзөр байхгүй: {required_count}")

if player2.has_cards(required_count):
    print(f"Тоглогч 2-д хангалттай хөзөр байна: {required_count}")
else:
    print(f"Тоглогч 2-д хангалттай хөзөр байхгүй: {required_count}")
