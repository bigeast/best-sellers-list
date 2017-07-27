from bs4 import BeautifulSoup
import bs4
import requests
from colorama import Fore, Back, Style
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

   ITALIC = '\e[3m'
   BOLD = '\e[1m'

L = [
        'combined-print-and-e-book-nonfiction',
        'combined-print-and-e-book-fiction',
        'hardcover-nonfiction',
        'hardcover-fiction',
        'paperback-nonfiction',
        'trade-fiction-paperback',
        'advice-how-to-and-miscellaneous',
        'business-books',
        'science',
        'sports'
        ]

def _html2text(htmlTag):
    # print('processing Tag ', htmlTag)
    if isinstance(htmlTag, bs4.element.NavigableString):
        return str(htmlTag)

    x = htmlTag
    res = ""
    if x.name == 'i':
        # print('Italic')
        res += color.ITALIC
        res += ''.join([_html2text(child) for child in x.children])
        res += color.END
        # print("res", res)
    elif x.name == 'b':
        # print('Bold')
        res += color.BOLD
        res += ''.join([_html2text(child) for child in x.children])
        res += color.END
        # print("res", res)
    elif x.name == 'p':
        res += ''.join([_html2text(child) for child in x.children])
        res += '\n'
    elif x.name == 'br':
        res += '\n'
    elif x.name == 'div' or x.name == 'span':
        res += ''.join([_html2text(child) for child in x.children])
    else:
        print(x)
        raise(ValueError)
    return res

def _getBS_NYT(bs_url, fresh=True, goodreadsDesc=False):
    r = requests.get(bs_url)
    soup = BeautifulSoup(r.text, 'lxml')
    books = soup.findAll('article', class_='book')
    idx = 0
    res = ""
    for item in books:
        idx += 1
        if fresh:
            freshness = item.findAll('p', class_='freshness')[0].text
        name = item.findAll('h2', class_='title')[0].text
        FCname = ' '.join([x[0] + x[1:].lower() for x in name.split(' ')])
        author = item.findAll('p', class_='author')[0].text
        publisher = item.findAll('p', class_='publisher')[0].text
        isbn = item.findAll('meta', {'itemprop': 'isbn'})[1]['content']
        print("getting description of book: " + FCname + " " + isbn)
        if goodreadsDesc:
            goodr = requests.get('https://www.goodreads.com/book/isbn/' + isbn)
            goodsoup = BeautifulSoup(goodr.text, 'lxml')
            descContainer = goodsoup.findAll('div', {'id': 'descriptionContainer'})
            if len(descContainer) != 0: # e.g. 9780399180842 does not exist.
                descs = descContainer[0].findAll('span')
                descriptionShort = _html2text(descs[0])
                descriptionFull = _html2text(descs[1])
                description = descriptionFull
            else:
                description = item.findAll('p', class_='description')[0].text.strip()
        else:
            description = item.findAll('p', class_='description')[0].text.strip()

        # print('#{}|{:^50}|'.format(idx, FCname) + '\t' + Fore.RED + Style.DIM + author + Style.RESET_ALL + ' ISBN: ' + isbn + Style.BRIGHT + ' ' + freshness + Style.RESET_ALL)
        # print('\t' + Fore.YELLOW + description + Style.RESET_ALL)
        # print('\n')

        # res += '#{}|{:^50}|'.format(idx, FCname) + '\t' + Fore.RED + Style.DIM + author + Style.RESET_ALL + ' ISBN: ' + isbn + ' ' + Style.BRIGHT + freshness + Style.RESET_ALL + '\n'
        # res += '\t' + Fore.YELLOW + description + Style.RESET_ALL + '\n\n\n'
        res += Fore.YELLOW + '#{}|{:^50}|'.format(idx, FCname) + Fore.RESET + '\t' + Fore.RED + author + Fore.RESET + ' ISBN: ' + isbn;
        if fresh:
            res += ' ' + Style.BRIGHT + freshness + Style.RESET_ALL + '\n'
        res += '\t' + Fore.GREEN + description + Fore.RESET + '\n\n\n'
    return res


desc_str = '\n'.join([str(x) for x in enumerate(L)])
while True:
    try:
        ch = input('which list do you want to get(press "h" for help): ')
        if ch == 'q':
            print('exiting...')
            break
        elif ch == 'h':
            parms = ['q', 'h', 'l', 'all', '[0-9]']
            descs = ['quit', 'help', 'list all', 'download all', 'download a list']
            print('\n'.join([color.RED + parms[i] + color.END + ': ' + descs[i] for i in range(len(parms))]))
            continue
        elif ch == 'l':
            print(desc_str)
            continue
        elif ch == 'all' or ch == '':
            print('will update all lists.')
            tobeUpdate = range(len(L))
        else:
            idx = int(ch)
            if 0 <= idx < len(L):
                print('downloading ' + L[idx])
                tobeUpdate = [idx]
            else:
                print("index out of range")
                continue
    except ValueError:
        print(color.RED + "Please enter a number" + color.END)
        continue
    for x in tobeUpdate:
        bs_url = 'https://www.nytimes.com/books/best-sellers/' + L[x]
        res = _getBS_NYT(bs_url, fresh=(x < 7), goodreadsDesc=True)
        fname = 'nyt_' + L[x] + '.txt'
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(res)
        print(res)
        print("check it out in " + fname)
