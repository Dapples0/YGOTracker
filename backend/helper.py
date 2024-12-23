import sys, os, time, math, re, enum

helpCommands = """
/q      -       Exits the program
/?      -       Prints list of commands
>       -       Go to next page
<       -       Return to previous page
"""

priceItemNum = 7
cardItemNum = 25

def checkCardDirs(dirName):
    os.chdir(os.path.dirname(__file__))
    if not os.path.exists(f"../{dirName}"):
        try:
            os.makedirs(f"../{dirName}")

        except OSError:
            print(f"{sys.argv[0]} : error: unable to create {dirName} directory")
            sys.exit(1)


def checkDatabaseDate():
    current_time = time.time()

    last_modified = os.stat("../.cardList").st_mtime

    day = 86400
    if last_modified < current_time - day * 2:
        os.remove("../.cardList/database")
        return True



    return False

def sortKey(item):
    if "Monster" in item["type"]:
        return 0
    elif "Spell" in item["type"]:
        return 1
    else:
        return 2

def cardDisplay(cardList, cardName):
    numCards = len(cardList)

    if numCards == 1:
        return cardList[0]["name"]

    numPages = math.ceil(numCards / cardItemNum)
    print(f"The following cards match \"{cardName}\":")
    i = 1

    loop_cards = True
    page_loop = True
    curPage = 1
    while loop_cards:
        page_loop = True
        card = cardList[i - 1]

        if i <= numCards:
            print(f"{str(i) + '.':<4}{card['name']:<55}|{card['race']:^20}|{card['type']:^25}")


        if i % cardItemNum == 0 or i == numCards:
            print(f"On page {curPage}/{numPages}")
            while page_loop:
                command, curPage, loop_cards, page_loop, i = dynamicPage(numCards, curPage, numPages, i, cardItemNum)
                if re.fullmatch(r'[1-9][0-9]*', command) and int(command) <= numCards and int(command) >= 1:
                    return cardList[int(command) - 1]["name"]
                elif command == "/q":
                    return ""
        i = i + 1

def getDeckList(ydkName):
    os.chdir(os.path.dirname(__file__))
    try:
        deckList = {
            "Main" : {},
            "Extra" : {},
            "Side" : {},
        }
        deckSpot = "main"
        with open(f"../decks/{ydkName}.ydk", "r") as f:
            for line in f:
                line = line.strip().rstrip('\n')
                if line == "#main":
                    deckSpot = "Main"
                    continue
                elif line == "#extra":
                    deckSpot = "Extra"
                    continue
                elif line == "!side":
                    deckSpot = "Side"
                    continue
                elif not re.match(r'^\d+$', line):
                    continue

                if line in deckList[deckSpot]:
                    deckList[deckSpot][line] += 1
                else:
                    deckList[deckSpot][line] = 1


        return deckList
    except OSError:
        print("tracker-error: input file must be a .ydk file in the decks folder", file=sys.stderr)
        sys.exit(1)



def dynamicPage(numItems, curPage, numPages, index, numDisplay):
    command = input("Enter Command/Card Number (/? for help): ")
    if command == ">" and curPage != numPages:
        curPage = curPage + 1
        return command, curPage, True, False, index
    elif command == "<" and curPage != 1:
        curPage = curPage - 1
        if index % numDisplay == 0:
            index = index - (numDisplay * 2)
        elif index == numItems:
            index = index - (index % numDisplay + numDisplay)
        return command, curPage, True, False, index
    elif command == "/q":
        return command, curPage, False, False, index
    elif command == "/?":
        print(helpCommands)
        return command, curPage, True, False, index


    return command, curPage, True, True, index

def displayPrice(cardInfo):
    numSets = len(cardInfo["card_sets"])
    print(f"{cardInfo['name']} | {cardInfo['attribute']} {cardInfo['race']} {cardInfo['type']} | Lvl {cardInfo['level']} | ATK/{cardInfo['atk']} DEF/{cardInfo['def']}")

    numPages = math.ceil(numSets / priceItemNum)

    i = 1

    loop_sets = True
    page_loop = True
    curPage = 1
    while loop_sets:
        page_loop = True
        set = cardInfo["card_sets"][i - 1]
        if i <= numSets:
            print(f"\t{set['set_name']}:\n\t\tSet Code: {set['set_code']}\n\t\tRarity: {set['set_rarity']}\n\t\tEdition: {set['set_edition']}\n\t\tPrice: {set['set_price']}\n")
        if i % priceItemNum == 0 or i == numSets:
            print(f"On page {curPage}/{numPages}")
            while page_loop:
                command, curPage, loop_sets, page_loop, i = dynamicPage(numSets, curPage, numPages, i, priceItemNum)
                if command == "/q":
                    break

        i = i + 1

def displayDeckPrice(deckList):
    totalPrice = 0.00

    for deckSpot in deckList:
        print(deckSpot + ":")
        deckSpotPrice = 0.00
        for card in deckList[deckSpot]:
            price = filterCardPrice(card[0]["card_prices"])
            sumPrice = price * card[1]
            print(f"\t{(card[0]['name'][:20] + '...') if len(card[0]['name']) > 20 else card[0]['name']:<25}({card[1]})\t|\tSingle Price: ${price:.2f}\t|\tSum Price: ${sumPrice:.2f}")
            deckSpotPrice += sumPrice
        print(f"{deckSpot} Deck Cost: ${deckSpotPrice:.2f}")
        totalPrice += deckSpotPrice
    print(f"Total Cost: ${totalPrice:.2f}")


def filterCardPrice(prices):
    if not prices:
        return 0.00
    return float(prices[0]["tcgplayer_price"])