import sys, os, time, math, re

helpCommands = """
/q      -       Exits the program
/?      -       Prints list of commands
>       -       Go to next page
<       -       Return to previous page
"""


def checkCardDirs():
    os.chdir(os.path.dirname(__file__))
    if not os.path.exists("../../.cardList"):
        try:
            os.makedirs("../../.cardList")

        except OSError:
            print(f"{sys.argv[0]} : error: unable to create .cardList directory")
            sys.exit(1)


def checkDatabaseDate():
    current_time = time.time()

    last_modified = os.stat("../../.cardList").st_mtime

    day = 86400
    if last_modified < current_time - day * 2:
        os.remove("../../.cardList/database")
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

    numPages = math.ceil(numCards / 25)
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


        if i % 25 == 0 or i == numCards:
            print(f"On page {curPage}/{numPages}")
            while page_loop:
                command, curPage, loop_cards, page_loop, i = dynamicPage(numCards, curPage, numPages, i, 25)
                if re.fullmatch(r'[1-9][0-9]*', command) and int(command) <= numCards and int(command) >= 1:
                    return cardList[int(command) - 1]["name"]
                elif command == "/q":
                    return ""
        i = i + 1

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
        # print(helpCommands)
        return command, curPage, True, False, index


    return command, curPage, True, True, index

def displayPrice(cardInfo):
    numSets = len(cardInfo["card_sets"])
    print(f"{cardInfo['name']} | {cardInfo['attribute']} {cardInfo['race']} {cardInfo['type']} | Lvl {cardInfo['level']} | ATK/{cardInfo['atk']} DEF/{cardInfo['def']}")

    numPages = math.ceil(numSets / 7)

    i = 1

    loop_sets = True
    page_loop = True
    curPage = 1
    while loop_sets:
        page_loop = True
        set = cardInfo["card_sets"][i -1]
        if i <= numSets:
            print(f"\t{set['set_name']}:\n\t\tSet Code: {set['set_code']}\n\t\tRarity: {set['set_rarity']}\n\t\tEdition: {set['set_edition']}\n\t\tPrice: {set['set_price']}\n")
        if i % 7 == 0 or i == numSets:
            print(f"On page {curPage}/{numPages}")
            while page_loop:
                command, curPage, loop_sets, page_loop, i = dynamicPage(numSets, curPage, numPages, i, 7)
                if command == "/q":
                    break

        i = i + 1