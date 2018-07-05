import requests
from bs4 import BeautifulSoup

URL = 'https://en.wikipedia.org/wiki/Mobile_country_code'
OUT = 'out.tsv'

def main():
    soup = BeautifulSoup(requests.get(URL).content, 'html.parser')
    tables = soup.find_all('table', attrs={'class':'wikitable'})

    with open(OUT, 'w') as f:
        [f.write(u'{0}{1}\t{2}\t{3}\n'.format(*cols[:4]).encode('utf8'))
            for table in tables
            for row in table.find_all('tr')
            for cols in [[col.text.strip() for col in row.find_all('td')]]
            if len(cols) > 3 and cols[2] != 'TEST'
        ]


if __name__ == '__main__':
    main()
