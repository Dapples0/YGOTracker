import sys, os, time, math, re

def checkCardDirs():
    if not os.path.exists("../../.cardInfo"):
        try:
            os.makedirs("../../.cardInfo")
            os.makedirs("../../.cardInfo/cardList")
            os.makedirs("../../.cardInfo/cardStore")

        except OSError:
            print(f"{sys.argv[0]} : error: unable to create .cardInfo directory")
            sys.exit(1)

    if not os.path.exists("../../.cardInfo/cardList"):
        try:
            os.makedirs("../../.cardInfo/cardList")
        except OSError:
            print(f"{sys.argv[0]} : error: unable to create cardList directory")
            sys.exit(1)

    if not os.path.exists("../../.cardInfo/cardStore"):
        try:
            os.makedirs("../../.cardInfo/cardStore")
        except OSError:
            print(f"{sys.argv[0]} : error: unable to create cardStore directory")
            sys.exit(1)

def checkDatabaseDate():

    current_time = time.time()

    last_modified = os.stat("../../.cardInfo/cardList/database").st_mtime

    day = 86400

    if last_modified < current_time - day * 2:
        os.remove("../../.cardInfo/cardList/database")
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
    curPage = 1
    while loop_cards:

        card = cardList[i - 1]

        if i <= numCards:
            print(f"{str(i) + '.':<4}{card['name']:<55}|{card['race']:^20}|{card['type']:^25}")

        if i % 25 == 0 or i == numCards:
            print(f"On page {curPage}/{numPages}")
            while True:
                command = input("Enter Command (? for help): ")
                if command == ">" and curPage != numPages:
                    curPage = curPage + 1
                    break
                elif command == "<" and curPage != 1:
                    curPage = curPage - 1
                    if i % 25 == 0:
                        i = i - 50
                    elif i == numCards:
                        i = i - (i % 25 + 25)
                    break
                elif command == "q":
                    loop_cards = False
                    break
                elif command.isnumeric and int(command) <= numCards and int(command) >= 1:
                    return cardList[int(command) - 1]["name"]

        i = i + 1

