# cardMan_model.py

# Картын утгууд ба өнгө
SUITS = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.value} of {self.suit}"

class CardManager:
    def __init__(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def show_hand(self):
        return ', '.join(map(str, self.hand))
    
    def sort_hand(self):
        self.hand.sort(key=lambda card: (VALUES[card.value], SUITS.index(card.suit)))

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

class AICardManager(CardManager):
    def __init__(self):
        super().__init__()

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

    def is_stronger_combo(self, combo, other_combo):
        """5 хөзрийн хослолыг харьцуулж хүчтэй эсэхийг тодорхойлно."""
        combo_value = self.evaluate_combo(combo)
        other_combo_value = self.evaluate_combo(other_combo)
        
        return combo_value > other_combo_value

    def evaluate_combo(self, combo):
        """Хослолын үнэлгээг тодорхойлно."""
        validator = FiveCardValidator(combo)
        return validator.evaluate_hand()

    def play_best_five_card_combo(self, last_played_combo):
        """AI хамгийн тохиромжтой 5 хөзрийн хослолыг тоглоно."""
        combo_to_play = self.choose_five_card_combo(last_played_combo)
        if combo_to_play:
            for card in combo_to_play:
                self.play_card(card)
            return combo_to_play
        else:
            return None  # Тоглох боломжгүй бол ямар ч хослолыг тоглохгүй

    def make_move(self, last_played_cards):
        """AI тоглогч хөдөлгөөн хийх."""
        if len(last_played_cards) == 5:  # Нөгөө тоглогчийн 5 хөзрөөр тоглосон эсэхийг шалгана
            card_combo = self.play_best_five_card_combo(last_played_cards)
            if card_combo:
                print(f"AI тоглогч тоглох 5 хөзрийн хослол: {card_combo}")
            else:
                print("AI тоглогч тоглох боломжгүй байна.")
        elif len(last_played_cards) == 3:  # Нөгөө тоглогчийн 3 карт тоглосон үед
            card_triple = self.play_best_triple(last_played_cards)
            if card_triple:
                print(f"AI тоглогч тоглох гурвалсан хослол: {card_triple}")
            else:
                print("AI тоглогч тоглох боломжгүй байна.")
        elif len(last_played_cards) == 2:  # Нөгөө тоглогчийн 2 карт тоглосон үед
            card_pair = self.play_best_pair(last_played_cards)
            if card_pair:
                print(f"AI тоглогч тоглох хослол: {card_pair}")
            else:
                print("AI тоглогч тоглох боломжгүй байна.")
        else:
            # 1 карт тоглосон тохиолдолд өмнөх стратеги ашиглана
            card = self.play_best_card(last_played_cards[0])
            if card:
                print(f"AI тоглогч тоглох карт: {card}")
            else:
                print("AI тоглогч тоглох боломжгүй байна.")

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
