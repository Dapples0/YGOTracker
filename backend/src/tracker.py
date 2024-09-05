from cardGet import getCardList, cardNameFind, getPriceInfo
from helper import cardDisplay, displayPrice, helpCommands
import argparse

parser = argparse.ArgumentParser(description='Tracks prices of Yu-Gi-Oh! cards and costs of decks.')
parser.add_argument('ydk_file', type=str, nargs='?',
                    help='a file with a ydk extension')
parser.add_argument('--f', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='selects deck pricing option')

args = parser.parse_args()

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
