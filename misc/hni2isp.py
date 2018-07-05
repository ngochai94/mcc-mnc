'''
    Generate a mapping from hni (= mcc + mnc) to network name
'''
import requests
from bs4 import BeautifulSoup

def sanitize(text):
    return ' '.join(text.strip().lower().replace('"', '').split())

def get_from_sms_carrier():
    soup = BeautifulSoup(requests.get('http://mcc-mnc.com/').content, 'html.parser')
    tables = soup.find_all('table', attrs={'id':'mncmccTable'})
    result = {}

    for table in tables:
        for row in table.find_all('tr'):
            cols = [sanitize(col.text) for col in row.find_all('td')]
            if len(cols) < 6:
                continue
            mcc, mnc, isp = cols[0], cols[1], cols[5]
            if isp:
                result[mcc + mnc] = isp

    return result

def get_from_wikipedia():
    url = 'https://en.wikipedia.org/wiki/Mobile_country_code'
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    tables = soup.find_all('table', attrs={'class':'wikitable'})
    result = {}

    for table in tables:
        data = {}
        br2op = {}
        for row in table.find_all('tr'):
            cols = [sanitize(col.text) for col in row.find_all('td')]
            if len(cols) < 4 or cols[2] == 'TEST' or not (cols[2] + cols[3]):
                continue
            mcc, mnc, brand, operator = cols[:4]
            data[mcc + mnc] = {'brand': brand, 'operator': operator}
            br2op[brand] = (br2op[brand] if brand in br2op else []) + [operator]

        for hni in data:
            brand = data[hni]['brand']
            operator = data[hni]['operator']
            if (len(set(br2op[brand])) < 3 or not brand) and operator:
                result[hni] = operator
            else:
                result[hni] = brand

    return result

def main():
    result = get_from_sms_carrier()
    mapping_from_wikipedia = get_from_wikipedia()
    for hni in mapping_from_wikipedia:
        if hni not in result:
            result[hni] = mapping_from_wikipedia[hni]

    with open('hni2isp.tsv', 'w') as f:
        for hni in result:
            f.write(u'{0}\t{1}\n'.format(hni, result[hni]).encode('utf8'))


if __name__ == '__main__':
    main()
