import sys, re, os, requests, json
from backend.helper import checkDatabaseDate, checkCardDirs, sortKey

url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

databasePath = "../.cardList/database"




def getCardList():
    checkCardDirs(".cardList")

    if not os.path.isfile(databasePath) or checkDatabaseDate():
        res = requests.get(url, params={
            "tcgplayer_data" : True
        })

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
                "id"   : card["id"],
                "name" : card["name"],
                "type" : card["type"],
                "race" : card["race"],
            }
            for card in data if re.search(cardName, card["name"], re.I)
        ]

        cardList = sorted(cardList, key=sortKey)



    return cardList

def getIdPriceInfo(cardId):
    with open(databasePath, "r") as f:
        data = json.load(f)
        cardInfo = [
            {
                "id"   : card["id"],
                "name" : card["name"],
                "type" : card["type"],
                "desc": card["desc"],
                "atk": card.get("atk", "N/A"),
                "def": card.get("def", "N/A"),
                "level": card.get("level", "N/A"),
                "race": card["race"],
                "attribute": card.get("attribute", "N/A"),
                "card_sets": card.get("card_sets", "N/A"),
                "card_prices": card["card_prices"],
            }
            for card in data if cardId == card["id"]
        ]

    if not cardInfo:
        return [
            {
                "id"   : int(cardId),
                "name" : "N/A",
                "type" : "N/A",
                "desc": "N/A",
                "atk": "N/A",
                "def": "N/A",
                "level": "N/A",
                "race": "N/A",
                "attribute": "N/A",
                "card_sets": [],
                "card_prices": [],
            }
        ][0]
    return cardInfo[0]


def getPriceInfo(cardName):
    with open(databasePath, "r") as f:
        data = json.load(f)
        cardInfo = [
            {
                "id"   : card["id"],
                "name" : card["name"],
                "type" : card["type"],
                "desc": card["desc"],
                "atk": card.get("atk", "N/A"),
                "def": card.get("def", "N/A"),
                "level": card.get("level", "N/A"),
                "race": card["race"],
                "attribute": card.get("attribute", "N/A"),
                "card_sets": card.get("card_sets", "N/A"),
                "card_prices": card["card_prices"],
            }
            for card in data if re.fullmatch(cardName, card["name"], re.I)
        ]

    return cardInfo[0]

def getDeckListPrice(deckListIds):
    deckList = {
        "Main" : [],
        "Extra" : [],
        "Side" : [],
    }

    for deckSpot in deckListIds:
        for cardId in deckListIds[deckSpot]:
            amount = deckListIds[deckSpot][cardId]
            cardInfo = getIdPriceInfo(int(cardId))
            deckList[deckSpot].append((cardInfo, amount))


    return deckList