from backend.cardGet import getCardList, cardNameFind, getDeckListPrice, getPriceInfo
from backend.helper import cardDisplay, checkCardDirs, displayDeckPrice, displayPrice, getDeckList, helpCommands
import argparse, sys

parser = argparse.ArgumentParser(prog="tracker", description='Tracks prices of Yu-Gi-Oh! cards and costs of decks.')
group = parser.add_argument_group('group')
group.add_argument('-f', '--file',  action='store_true',
                    help='selects deck pricing option')
group.add_argument('ydk_file', type=str, nargs='?',
                    help='a file with a ydk extension')

args = parser.parse_args()

if (not args.file and args.ydk_file is not None) or (args.file and args.ydk_file is None):
    parser.print_help()
    sys.exit(1)


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

            if len(cardName) == 0:
                continue

            cardInfo = getPriceInfo(cardName)

            displayPrice(cardInfo)

def menus_decklist():
    ydkName = args.ydk_file.strip().rstrip(".ydk")

    checkCardDirs("decks")

    print("Calculating Deck Price...")

    deckList = getDeckListPrice(getDeckList(ydkName))

    displayDeckPrice(deckList)

if __name__ == "__main__":
    print("Loading database...")
    getCardList()
    if args.file:
        menus_decklist()
    else:
        menus_loop()
