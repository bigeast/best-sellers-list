from bs4 import BeautifulSoup
import requests
from colorama import Fore, Back, Style

def _getBS_NYT(bs_url):
    r = requests.get(bs_url)
    soup = BeautifulSoup(r.text, 'lxml')
    books = soup.findAll('article', class_='book')
    idx = 0
    res = ""
    for item in books:
        idx += 1
        freshness = item.findAll('p', class_='freshness')[0].text
        name = item.findAll('h2', class_='title')[0].text
        FCname = ' '.join([x[0] + x[1:].lower() for x in name.split(' ')])
        author = item.findAll('p', class_='author')[0].text
        publisher = item.findAll('p', class_='publisher')[0].text
        description = item.findAll('p', class_='description')[0].text.strip()
        isbn = item.findAll('meta', {'itemprop': 'isbn'})[1]['content']
        # print('#{}|{:^50}|'.format(idx, FCname) + '\t' + Fore.RED + Style.DIM + author + Style.RESET_ALL + ' ISBN: ' + isbn + Style.BRIGHT + ' ' + freshness + Style.RESET_ALL)
        # print('\t' + Fore.YELLOW + description + Style.RESET_ALL)
        # print('\n')
        res += '#{}|{:^50}|'.format(idx, FCname) + '\t' + Fore.RED + Style.DIM + author + Style.RESET_ALL + ' ISBN: ' + isbn + ' ' + Style.BRIGHT + freshness + Style.RESET_ALL + '\n'
        res += '\t' + Fore.YELLOW + description + Style.RESET_ALL + '\n\n\n'
    return res

L = ['combined-print-and-e-book-nonfiction','combined-print-and-e-book-fiction','hardcover-fiction','hardcover-nonfiction','paperback-nonfiction']

for item in L:
    bs_url = 'https://www.nytimes.com/books/best-sellers/' + item
    res = _getBS_NYT(bs_url)
    with open('nyt_' + item + '.txt', 'w', encoding='utf-8') as f:
        f.write(res)
