import argparse, sys, requests, humanize
from parseURL import parseURL

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-u', '--url', dest='url', type=str, required=True,
                    help='destination youtube video url')
parser.add_argument('-o', dest='output', type=str, metavar='path/to/file',
                    help='specify output')
parser.add_argument('-r', '--resolution', dest='resolution', type=str,
                    help='hint resolution')
parser.add_argument('-v', dest='verbose', action='store_true',
                    help='Verbose mode')

args = parser.parse_args()

def progess_bar(current, total):
    bar_length = 25
    percent = float(current) / float(total)
    hashes = '#' * int(round(percent * bar_length))
    spaces ='_' * (bar_length - len(hashes))
    sys.stdout.write(f'\r{current}/{total} bytes   [{hashes}{spaces}] {int(round(percent * 100))}%')
    sys.stdout.flush()

def main(): 
    data = parseURL(args.url)
    print("Video", data['title'])

    key = 0
    for i in data['files']:
        print(f"[{key}]", i['quality'], i['type'], ' - ', i['size'])
        key += 1
    
    resolution = input('[+] Resolution: ')
    file = data['files'][int(resolution)]
    response = requests.get(file['url'], stream=True)

    total = int(response.headers['Content-length'])
    current = 0
    with open(f"{data['title']}.{file['type']}", "wb") as handle:
        for data in response.iter_content(chunk_size=1024):
            progess_bar(current, total)
            handle.write(data)
            current += 1024

if __name__ == "__main__":
    main()