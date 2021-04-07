from bs4 import BeautifulSoup
import requests
from errors import *
from re import sub
import re

class Gamescraper:

    def getPrice(url, subId):
        try:
            page = requests.get(url)
            data = page.text
            soup = BeautifulSoup(data, 'html.parser')
            content = soup.find("div", {"id": subId})
            if content == None:
                content = soup.find("div", {"data-ds-itemkey": subId})
            try:
                text = content.find("div", {"class": "discount_final_price"}).text.strip()
            except:
                text = content.find("div", {"class": "game_purchase_price price"}).text.strip()
            return text
        except:
            raise FindPriceError(url, subId)

    def compressEntry(entry):
        if entry == "":
            raise InputError("No context")
        entryList = entry.split()
        url = entryList[len(entryList)-1]
        del entryList[len(entryList)-1]
        name = " ".join(entryList)
        try:
            page = requests.get(url)
            data = page.text
            soup = BeautifulSoup(data, 'html.parser')
            gameList = soup.findAll("div", {"class": "game_area_purchase_game"})
        except:
            raise InputError(entry)
        for element in gameList:
            text = element.find("h1").text.strip()
            text = text.replace("(?)", "")
            text = text.replace("\n", "")
            text = text.replace("\r", "")
            text = re.sub(r'\t.+\t', '', text)
            if text == name or len(entryList) == 0:
                if element.has_attr("id"):
                    subId = element.attrs["id"]
                    return url, subId, text
                elif element.parent.has_attr("data-ds-itemkey"):
                    subId = element.parent.attrs["data-ds-itemkey"]
                    return url, subId, text
        raise NoGameError(entry)

    def convertPriceToFloat(price):
        priceString = sub(r'[^\d,]', '', price)
        return float(priceString.replace(',', '.'))