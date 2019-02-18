from html.parser import HTMLParser
import html
import requests
from sys import argv
import re

class CustomHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.words = dict()
        self.is_title = False
        self.stack = list()
        self.ingnor_tags = set({"meta", "br"})
    def handle_starttag(self, tag, attrs):
        if tag in self.ingnor_tags:
            return
        self.stack.append(tag)
        if (len(self.title) == 0) and (tag == "title"):
            self.is_title = True

    def handle_endtag(self, tag):
        if tag in self.ingnor_tags:
            return
        self.stack.pop()
        if tag == "title":
            self.is_title = False

    def handle_data(self, data):
        if self.is_title:
            self.title = self.title + data
        if (len(self.stack) > 0) and (self.stack[-1] == 'div'):
            data = html.unescape(data).lower()
            data = re.sub(r'[^A-Za-z]', ' ', data)
            word_lst = data.split()
            for word in word_lst:
                self.words[word] = self.words.get(word, 0) + 1

if len(argv) < 2:
    print("Enter URL")
    exit(0)

regex = re.compile(
        r'^(?:http)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

if re.match(regex, argv[1]) is None:
    print("Invalid url")
    exit(0)

try:
    r = requests.get(argv[1])
except:
    print("Can't download page {}".format(argv[1]))
    exit(0)

if r.status_code != requests.codes.ok:
    print("Error: http status not ok")
    exit(0)

parser = CustomHTMLParser()
parser.feed(r.text)
stop_words = ["a", "about", "above", "after", "again", "against", "all", "am",
              "an", "and", "any", "are", "aren't", "as", "at", "be", "because",
              "been", "before", "being", "below", "between", "both", "but", "by",
              "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does",
              "doesn't", "doing", "don't", "down", "during", "each", "few", "for",
              "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
              "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers",
              "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
              "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its",
              "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no",
              "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
              "our", "ours", "ourselves", "out", "over", "own", "same", "shan't",
              "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some",
              "such", "than", "that", "that's", "the", "their", "theirs", "them",
              "themselves", "then", "there", "there's", "these", "they", "they'd",
              "they'll", "they're", "they've", "this", "those", "through", "to",
              "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd",
              "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when",
              "when's", "where", "where's", "which", "while", "who", "who's", "whom",
              "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd",
              "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]

for word in stop_words:
    parser.words[word] = 0

sorted_x = sorted(parser.words.items(), key=lambda x: (-x[1],x[0]))
print(parser.title+"\n")
for item in sorted_x:
    if item[1] > 0:
        print("{:10}\t{}".format(item[0], item[1]))