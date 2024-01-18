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

def getTitle(content: str) -> str:
    return re.search(r"<title[\s\n]*>[\s\n]*(.*)[\s\n]*</title[\s\n]*>", content).group(1)[:-10]

def getChannel(content: str) -> str:
    return re.search(r"<link itemprop=\"name\" content=\"(.*?)\">", content).group(1)

def getThumbnail(url: str) -> str:
    video_id = url.split('?v=')[1]
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

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

def parseURL(url: str) -> dict:
    res = requests.get(url, headers={'User-Agent': user_agent})
    content = res.content.decode()
    files = parseDL(content)
    title = getTitle(content)
    channel = getChannel(content)
    thumbail = getThumbnail(url)

    data = {
        'title': title,
        'channel': channel,
        'files': files,
        'thumbail': thumbail
    }

    return data

if __name__ == "__main__":
    import sys
    sys.exit("This is a module, not a script")