import re, requests
import json
import pprint

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"

def checkType(string: str) -> (str, str):
    splited: str = string.split(";")[0]
    type: str = splited.split('/')[0]
    subtype: str = splited.split('/')[1]
    return (type, subtype)

def byPasser():
    pass

def parseDL(content: str):
    script: str = re.search(r"var ytInitialPlayerResponse = ({.*?});", content).group(1)

    loaded: json = json.loads(script)
    data: json = loaded["streamingData"]["adaptiveFormats"]

    for i in data:
        if checkType(i["mimeType"])[0] == "video":
            print(str(i['width']) + " -> " + i["url"])
        else:
            print(i["url"])

def parseURL(url):
    res = requests.get(url, headers={'User-Agent': user_agent})
    content = res.content.decode()
    parseDL(content)


#parseURL('https://www.youtube.com/watch?v=Tc0M68TlBqc')
parseURL('https://www.youtube.com/watch?v=kplNazHyHt4')