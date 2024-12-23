# YGOTracker
CLI based Yu-Gi-Oh! singles and deck price tracker. Made using python and YGOProDeck API.

# Installation and setting up
Clone the repository into your device:
```sh
git clone git@github.com:Dapples0/Xdle.git
```

# How to use
Move to the root directory
```sh
cd YGOTracker
```

## Tracking specific cards
Run this line on your terminal to run the program
```sh
python3 tracker.py
```
Afterwards, you will be prompted to type in a card name (not case sensitive). If multiple cards match, input the cards respective number into the terminal.

## Getting the price a deck
To get the total price of a deck, the deck's ydk file must be in the "decks" folder. Once done, run this line on your terminal, where "deck-name.ydk" should be your ydk file.
```sh
python3 tracker.py -f "deck-name.ydk"
```

# (Self-Reflection) Future additions and improvements
1. Loosen dependency of front-end with back-end functions.

# Issues and edges cases
If any issues occur when using this program, open a new issue describing it and the steps to replicate it.