from bs4 import BeautifulSoup
import requests
from colorama import Fore, Back, Style
import json
import copy
class AmazonBook:
    isEbook = False
    name = ''
    author = ''
    rank = ''
    avg_stars = ''
    num_reviews = ''
    price = ''
    pages = ''
    publisher = ''
    isbn = ''
    asin = ''
    publishDate = ''

def getBS_AmazonCN():
    bs_url = 'https://www.amazon.cn/gp/bestsellers/books/'
    r = requests.get(bs_url)
    soup = BeautifulSoup(r.text, 'lxml')
    Books = []
    for item in soup.findAll('div', {'class': 'zg_itemRow'}):
        b = AmazonBook()
        b.isEbook = False

        b.asin = json.loads(item.findAll('div', {'class': 'p13n-asin'})[0]['data-p13n-asin-metadata'])['asin']
        b.rank = item.findAll('span', {'class': 'zg_rankNumber'})[0].text.strip()
        b.name = item.findAll('img')[0]['alt']

        try:
            b.author = item.findAll('span', {'class': 'a-color-base'})[0].text
        except:
            pass
        try:
            b.price = item.findAll('span', {'class': 'a-color-price'})[0].text
        except:
            pass

        try:
            icon_row = item.findAll('div', {'class': 'a-icon-row'})[0]
            b.avg_stars = icon_row.findAll(True, {'class': 'a-icon-star'})[0].text.strip()
            b.num_reviews = icon_row.findAll(True, {'class': 'a-size-small'})[0].text.strip()
        except:
            pass
        # b.asin = 'https://www.amazon.cn/dp/' + b.asin
        Books.append(copy.copy(b))

    res = Fore.YELLOW + "图书销售排行榜:" + Fore.RESET + '\n\t' + '\n\t'.join([book.rank + ' ' + Style.BRIGHT + book.name + Style.RESET_ALL + ' ' + Fore.CYAN + book.price + Fore.RESET + ' ' + Style.DIM + book.asin + Style.RESET_ALL + ' ' + Fore.MAGENTA + book.avg_stars + Fore.RESET + ' ' + Fore.GREEN + book.num_reviews + Fore.RESET + ' ' + Fore.GREEN + book.publishDate + Fore.RESET for book in Books]) + '\n'

    with open('amazon_book_top' + '_CN.txt', 'w', encoding='utf-8') as f:
        f.write(res)
    print(res)

def getBS_KindleCN():
    bs_url = 'https://www.amazon.cn/gp/bestsellers/digital-text'
    r = requests.get(bs_url)
    soup = BeautifulSoup(r.text, 'lxml')
    # ASIN lists
    notfree = []
    free = []
    b = AmazonBook()
    b.isEbook = True
    for item in soup.findAll('div', {'class': 'zg_itemRow'}):
        items = item.findAll('div', {'class': 'zg_item_compact'});

        links = [x.text.strip() for x in item.findAll('a')]
        info = json.loads(items[0].div['data-p13n-asin-metadata'])
        b.name = links[1].strip()
        b.avg_stars = links[2].strip()
        b.num_reviews = links[3].strip()
        b.asin = info['asin']
        notfree.append(copy.copy(b))

        info = json.loads(items[1].div['data-p13n-asin-metadata'])
        b.name = links[5].strip()
        b.avg_stars = links[6].strip()
        b.num_reviews = links[7].strip()
        b.asin = info['asin']
        free.append(copy.copy(b))
    res = Fore.YELLOW + "付费排行：" + Fore.RESET + '\n\t' + '\n\t'.join([book.rank + ' ' + Style.BRIGHT + book.name + Style.RESET_ALL + ' ' + Style.DIM + book.asin + Style.RESET_ALL + ' ' + Fore.MAGENTA + book.avg_stars + Fore.RESET + ' ' + Fore.GREEN + book.num_reviews + Fore.RESET + ' ' + Fore.GREEN + book.publishDate + Fore.RESET for book in notfree]) + '\n' + Fore.YELLOW + "免费排行：" + Fore.RESET + '\n\t' + '\n\t'.join([book.rank + ' ' + Style.BRIGHT + book.name + Style.RESET_ALL + ' ' + Style.DIM + book.asin + Style.RESET_ALL + ' ' + Fore.MAGENTA + book.avg_stars + Fore.RESET + ' ' + Fore.GREEN + book.num_reviews + Fore.RESET + ' ' + Fore.GREEN + book.publishDate + Fore.RESET for book in free]) + '\n'

    with open('amazon_kindle_top_CN.txt', 'w', encoding='utf-8') as f:
        f.write(res)
    print(res)



def getBS_KindleCOM(isfree=False):
    bs_url = 'https://www.amazon.com/gp/bestsellers/digital-text/'
    if isfree:
        bs_url += '?tf=1'
    r = requests.get(bs_url)
    soup = BeautifulSoup(r.text, 'lxml')
    # ASIN lists
    Books = []
    for item in soup.findAll('div', {'class': 'zg_itemImmersion'}):
        b = AmazonBook()
        b.isEbook = True
        b.asin = json.loads(item.findAll('div', {'class': 'p13n-asin'})[0]['data-p13n-asin-metadata'])['asin']
        b.rank = item.findAll('span', {'class': 'zg_rankNumber'})[0].text.strip()
        b.name = item.findAll('img')[0]['alt']

        try:
            b.author = item.findAll('div', {'class': 'a-row'})[0].text.strip()
        except:
            pass

        try:
            icon_row = item.findAll('div', {'class': 'a-icon-row'})[0]
            b.avg_stars = icon_row.findAll(True, {'class': 'a-icon-star'})[0].text.strip()
            b.num_reviews = icon_row.findAll(True, {'class': 'a-size-small'})[0].text.strip()
        except:
            pass

        try:
            b.publishDate = item.findAll('div', {'class': 'zg_releaseDate'})[0].text
        except:
            pass

        Books.append(copy.copy(b))
    res = Fore.YELLOW + "Top " + ("Free：" if isfree else "Paid: ") + Fore.RESET + '\n\t' + '\n\t'.join([book.rank + ' ' + Style.BRIGHT + book.name + Style.RESET_ALL + ' ' + Style.DIM + book.asin + Style.RESET_ALL + ' ' + Fore.MAGENTA + book.avg_stars + Fore.RESET + ' ' + Fore.GREEN + book.num_reviews + Fore.RESET + ' ' + Fore.GREEN + book.publishDate + Fore.RESET for book in Books]) + '\n'

    with open('amazon_kindle_top_' + ('free' if isfree else 'paid') + '.txt', 'w', encoding='utf-8') as f:
        f.write(res)
    print(res)



def getBS_AmazonCOM(pages=1):
    res = Fore.YELLOW + "Top Books" + Fore.RESET + '\n'
    bs_url = 'https://www.amazon.com/gp/bestsellers/books/'

    for page in range(pages):
        r = requests.get(bs_url + '?pg=' + str(page + 1))
        soup = BeautifulSoup(r.text, 'lxml')
        Books = []
        for item in soup.findAll('div', {'class': 'zg_itemImmersion'}):
            b = AmazonBook()
            b.isEbook = True
            b.asin = json.loads(item.findAll('div', {'class': 'p13n-asin'})[0]['data-p13n-asin-metadata'])['asin']
            b.rank = item.findAll('span', {'class': 'zg_rankNumber'})[0].text.strip()
            b.name = item.findAll('img')[0]['alt']

            try:
                b.author = item.findAll('div', {'class': 'a-row'})[0].text.strip()
            except:
                pass

            try:
                icon_row = item.findAll('div', {'class': 'a-icon-row'})[0]
                b.avg_stars = icon_row.findAll(True, {'class': 'a-icon-star'})[0].text.strip()
                b.num_reviews = icon_row.findAll(True, {'class': 'a-size-small'})[0].text.strip()
            except:
                pass

            try:
                b.publishDate = item.findAll('div', {'class': 'zg_releaseDate'})[0].text
            except:
                pass

            Books.append(copy.copy(b))
        res += '\t' + '\n\t'.join([book.rank + ' ' + Style.BRIGHT + book.name + Style.RESET_ALL + ' ' + Style.DIM + book.asin + Style.RESET_ALL + ' ' + Fore.MAGENTA + book.avg_stars + Fore.RESET + ' ' + Fore.GREEN + book.num_reviews + Fore.RESET + ' ' + Fore.GREEN + book.publishDate + Fore.RESET for book in Books]) + '\n'

    with open('amazon_book_top' + '.txt', 'w', encoding='utf-8') as f:
        f.write(res)
    print(res)

getBS_AmazonCN()
getBS_KindleCN()
getBS_AmazonCOM()
getBS_KindleCOM()
