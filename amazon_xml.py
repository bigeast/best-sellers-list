from bs4 import BeautifulSoup
import requests
from colorama import Fore, Back, Style
def _getBS_Amazon(bs_url):
    r = requests.get(bs_url)
    soup = BeautifulSoup(r.text, 'xml')
    pubDate = soup.find('pubDate')
    items = [x.findAll('title')[0].text for x in soup.findAll('item')]
    res = ""
    res += Style.DIM + pubDate.text + Style.RESET_ALL + '\n'
    for item in items:
        res += '\t' + Fore.MAGENTA + item + Fore.RESET + '\n'
    return res

def getBS_KindleCN():
    bs_url = 'https://www.amazon.cn/gp/rss/bestsellers/digital-text'
    return _getBS_Amazon(bs_url)

def getBS_KindleCOM():
    bs_url = 'https://www.amazon.com/gp/rss/bestsellers/digital-text'
    return _getBS_Amazon(bs_url)

def getBS_AmazonCN():
    bs_url = 'https://www.amazon.cn/gp/rss/bestsellers/books'
    return _getBS_Amazon(bs_url)

def getBS_AmazonCOM():
    bs_url = 'https://www.amazon.com/gp/rss/bestsellers/books'
    return _getBS_Amazon(bs_url)

res = ""
res += Style.BRIGHT + "实体书 " + Style.RESET_ALL
bs_url = 'https://www.amazon.cn/gp/rss/bestsellers/books'
res += _getBS_Amazon(bs_url)
res += Style.BRIGHT + "Kindle电子书 " + Style.RESET_ALL
bs_url = 'https://www.amazon.cn/gp/rss/bestsellers/digital-text'
res += _getBS_Amazon(bs_url)
res += Style.BRIGHT + "Paper Books" + Style.RESET_ALL
bs_url = 'https://www.amazon.com/gp/rss/bestsellers/books'
res += _getBS_Amazon(bs_url)
res += Style.BRIGHT + "Ebooks " + Style.RESET_ALL
bs_url = 'https://www.amazon.com/gp/rss/bestsellers/digital-text'
res += _getBS_Amazon(bs_url)

print(res)
with open('amazon_all.txt', 'w', encoding='utf-8') as f:
    f.write(res)
