from cardGet import getCardList, cardNameFind, getPriceInfo
from helper import cardDisplay, displayPrice
helpCommands = """
/q      -       Exits the program
/?      -       Prints list of commands
"""

def menus_loop():
    cardName = ""
    while True:
        cardName = input("Enter card name (/? for list of commands): ")

        if cardName == "/?":
            print(helpCommands)
        elif cardName == "/q":
            break

        cardList = cardNameFind(cardName)

        if len(cardList) == 0 and cardName != "/q":
            print(f"No cards that include \"{cardName}\" exists")
        else:
            cardName = cardDisplay(cardList, cardName)

            cardInfo = getPriceInfo(cardName)

            displayPrice(cardInfo)

if __name__ == "__main__":
    getCardList()
    menus_loop()
