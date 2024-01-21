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
    percent = current / total * 100
    bar_size = 20
    bar = '#' * int(round(percent / 100 * bar_size))
    empty ='_' * (bar_size - len(bar))
    sys.stdout.write(f'\r{humanize.naturalsize(current)}\{humanize.naturalsize(total)} [{bar}{empty}] {int(round(percent))}% completed')
    sys.stdout.flush()

def main(): 
    data = parseURL(args.url)
    print("========================================")
    print("[+] Video", data['title'])
    print("[+] Channel", data['channel'])
    print("========================================")

    key = 0
    for i in data['files']:
        print(f"[{key}]", i['quality'], i['type'], ' - ', i['size'])
        key += 1
    
    resolution = input('[+] Resolution: ')
    file = data['files'][int(resolution)]
    response = requests.get(file['url'], stream=True)

    total = int(response.headers['Content-length'])

    if args.output:
        title = args.output
    else:
        title = data['title'] + '.' + file['type']

    if args.verbose:
        print(f'[+] Downloading {title}...')
    
        with open(title, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    progess_bar(f.tell(), total)
    

if __name__ == "__main__":
    main()