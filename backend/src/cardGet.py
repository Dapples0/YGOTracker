import sys, re, os, requests, json

from helper import checkDatabaseDate, checkCardDirs, sortKey

url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

databasePath = "../../.cardInfo/cardList/database"





def getCardList():
    checkCardDirs()

    if not os.path.isfile(databasePath) or checkDatabaseDate():
        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()

            filtered_data = [
                {
                    "id" : card["id"],
                    "name": card["name"],
                    "type": card["type"],
                    "desc": card["desc"],
                    "atk": card.get("atk", "N/A"),
                    "def": card.get("def", "N/A"),
                    "level": card.get("level", "N/A"),
                    "race": card["race"],
                    "attribute": card.get("attribute", "N/A"),
                    "card_sets": card.get("card_sets", "N/A"),
                    "card_prices": card["card_prices"],
                }
                for card in data["data"]
            ]

            with open(databasePath, "w") as f:
                json.dump(filtered_data, f, indent=4)
        else:
            print(f"{sys.argv[0]} : error: unable to make API call : response code {res}", file=sys.stderr)
            sys.exit(1)

def cardNameFind(cardName):
    cardList = []
    with open(databasePath, "r") as f:
        data = json.load(f)
        cardList = [
            {
                "name" : card["name"],
                "type" : card["type"],
                "race" : card["race"],
            }
            for card in data if re.search(cardName, card["name"], re.I)
        ]

        cardList = sorted(cardList, key=sortKey)



    return cardList

def getPriceInfo(cardName, cardList):
    print(cardList)