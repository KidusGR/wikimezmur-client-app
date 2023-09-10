#!/usr/bin/python3

import requests
import json
from bs4 import BeautifulSoup
import pprint
import traceback

check = json.load(open("check.json"))
pre = check['data']['urls']['pre']


def getHome():
    res = requests.get(check['data']['urls']['home'])
    soup = BeautifulSoup(res.text, 'lxml')

    divs = soup.find_all("div")

    data = {
        "posts": [],
        "new": [],
        "stats": []
    }

    for div in divs:
        try:
            if div["style"] == check['data']['styles']['home']['post']:
                data["posts"].append(
                    {
                        "type": "artist",
                        "title": div.b.a['title'],
                        "href": f"{pre}{div.b.a['href']}",
                        "img": f"{pre}{div.img['src']}",
                        "amTitle": div.b.a.text
                    }
                )

        except Exception as e:
            e = e
            # traceback.print_exc()

        try:
            if div["style"] == check['data']['styles']['home']['new']:
                if "አዲስ!" in div.text:
                    for a in div.find_all("a"):
                        data["new"].append(
                            {
                                "type": "track",
                                "title": a['title'],
                                "href": f"{pre}{a['href']}",
                                "amTitle": a.text
                            }
                        )
        except Exception as e:
            e = e
            # traceback.print_exc()

        statStyles = check['data']['styles']['home']['stats']

        try:
            if div["style"] in statStyles:
                data["stats"].append((div.text).strip())
        except Exception as e:
            e = e
            # traceback.print_exc()

    return data


def getArtists(language=None):
    links = list(check['data']['urls']['artists'].values())
    artistStyles = check['data']['styles']['artists']

    data = {"artists": []}

    for link in links:
        res = requests.get(f"{link}")
        soup = BeautifulSoup(res.text, 'lxml')

        tables = soup.find_all("table")

        for table in tables:
            try:
                if table.td["style"] in artistStyles:

                    for a in table.find_all("a"):
                        data["artists"].append(
                            {
                                "title": a["title"].split("/")[-1] if "/" in a
                                ["title"] else a["title"],
                                "href": f'{pre}{a["href"]}',
                                "amTitle": a.text.split("(")[0].strip() if "("
                                in a.text else None,
                                "type": "artist"
                            }
                        )
            except Exception as e:
                e = e
                # traceback.print_exc()

    return data


def getAlbums():
    pass


pprint.pprint((getHome()))
pprint.pprint((getArtists()))
