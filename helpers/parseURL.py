import re, requests
import json
import pprint

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"

def checkType(string: str) -> (str, str):
    splited: str = string.split(";")[0]
    type: str = splited.split('/')[0]
    subtype: str = splited.split('/')[1]
    return (type, subtype)

def getSize(url: str) -> str:
    return requests.get(url, stream=True).headers['Content-length']

def byPasser():
    pass

def parseDL(content: str) -> list:
    script: str = re.search(r"var ytInitialPlayerResponse = ({.*?});", content).group(1)

    loaded: json = json.loads(script)
    data: json = loaded["streamingData"]["adaptiveFormats"]

    files = []

    for i in data:
        j = {}
        type = checkType(i["mimeType"])
        j['url'] = i['url']
        j['size'] = getSize(i['url'])
        j['type'] = type[1]
        if type[0] == "video":           
            j['width'] = str(i['width'])
        files.append(j)
    
    return files

def parseURL(url):
    res = requests.get(url, headers={'User-Agent': user_agent})
    content = res.content.decode()
    files = parseDL(content)

    print(files)


#parseURL('https://www.youtube.com/watch?v=Tc0M68TlBqc')
parseURL('https://www.youtube.com/watch?v=kplNazHyHt4')