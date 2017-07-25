from bs4 import BeautifulSoup
import requests
from colorama import Fore, Back, Style
def _getBS_Amazon(bs_url):
    r = requests.get(bs_url)
    soup = BeautifulSoup(r.text, 'xml')
    pubDate = soup.find('pubDate')
    items = [x.findAll('title')[0].text for x in soup.findAll('item')]
    print(Style.DIM + pubDate.text + Style.RESET_ALL)
    for item in items:
        print(Fore.YELLOW + item)

def getBS_KindleCN():
    bs_url = 'https://www.amazon.cn/gp/rss/bestsellers/digital-text'
    _getBS_Amazon(bs_url)

def getBS_KindleCOM():
    bs_url = 'https://www.amazon.com/gp/rss/bestsellers/digital-text'
    _getBS_Amazon(bs_url)

def getBS_AmazonCN():
    bs_url = 'https://www.amazon.cn/gp/rss/bestsellers/books'
    _getBS_Amazon(bs_url)

def getBS_AmazonCOM():
    bs_url = 'https://www.amazon.com/gp/rss/bestsellers/books'
    _getBS_Amazon(bs_url)
