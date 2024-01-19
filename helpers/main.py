import argparse

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
print(args.url)

