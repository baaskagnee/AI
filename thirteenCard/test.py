import tkinter as tk
from PIL import Image, ImageTk  # PIL-ийг зурагны загварчлалд ашиглана

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.image_path = f'images/{value}_of_{suit}.png'  # Картын зургийн зам

    def __repr__(self):
        return f'{self.value} of {self.suit}'

class CardGUI:
    def __init__(self, root, card):
        self.root = root
        self.card = card

        # Зургийг ачаалах
        self.image = Image.open(self.card.image_path)
        self.photo = ImageTk.PhotoImage(self.image)

        # Зургийг Tkinter интерфейс дээр харуулах
        self.label = tk.Label(root, image=self.photo)
        self.label.pack()

# Жишээ карт үүсгэх
root = tk.Tk()
card = Card('3', 'hearts')
card_gui = CardGUI(root, card)

root.mainloop()
