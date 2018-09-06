import requests
import time
import json
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
import csv




# Metadata
today = time.strftime("%m/%d").lstrip('0')

user_agent_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
            'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
            'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'
        ]

proxy_ips = [
    '51.15.227.220:3128',
    '81.162.56.154:8081',
    '61.133.222.67:8080',
    '117.177.243.6:8080',
    '117.127.0.209:80',
    '117.127.0.195:80',
    '117.127.0.198:8080'
    ]

# limitation
# https://tw.buy.yahoo.com/robots.txt

def main():
    url = 'https://tw.buy.yahoo.com/help/helper.asp?p=sitemap&hpp=sitemap'
    output = get_web_page(url)
    get_sublist(output)
    # count = get_articles(output)


def get_web_page(url, encode='utf-8'):
    # user agent
    usl = random.choice(user_agent_list)
    headers = {'User-Agent': usl}
    # proxy ip
    ip = random.choice(proxy_ips)
    # try and exception
    try:
        # Add header and proxy to get url
        resp = requests.get(url, headers=headers, proxies={'http': 'http://' + ip})
        # Solve garbled code
        resp.encoding = encode
        if resp.status_code == 200:
            print('Connection is working')
            return resp.text

    except Exception as e:
        print('Connection is failed. Invalid url:', resp.url)
        return None


def get_sublist(dom):
    soup = BeautifulSoup(dom, 'html5lib')
    sublist = []
    subname = {}
    for li in soup.find_all('li', {'class': 'site-list'}):
        sub = li.a['href'].split('=')[1]
        sublist.append(sub)
        subname[sub] = li.a.text
    return sublist, subname



def get_catid_catitemid(dom, sublist):
    soup = BeautifulSoup(dom, 'html5lib')
    catid = []
    catitemid = []
    sub2name = dict()
    sub3name = dict()
    for li in soup.find_all('h3', {'class': 'stitle'}):
        if li.a:
            sub2 = li.find('a')['href'].split('=')[1]
            sub2name[sub2] = li.find('a').text
            catid.append([sublist, sub2])

            for nli in li.parent.ul.find_all('li', {'class': 'list'}):
                sub3 = nli.a['href'].split('=')[1]
                sub3name[sub3] = nli.a.text
                catitemid.append([sub2, sub3])

    return catid, catitemid, sub2name, sub3name


# Get top 10 product information in each yahoo-defined categories
def get_top_sell(subcode, level, parentcode):
    url_part1 = 'https://tw.search.buy.yahoo.com/amp/search/shopping/product?cid='
    url_part2 = '&clv='
    url_part3 = '&flc=&flt=&pg=1&sort=-tsales'

    subcode = str(subcode)
    level = str(level)
    url = url_part1+subcode+url_part2+level+url_part3
    resp = get_web_page(url)

    soup = BeautifulSoup(resp, 'html5lib')
    count = 0
    item = []
    for li in soup.find('ul', 'gridList').find_all('li', {'class': 'BaseGridItem__grid___2wuJ7 imprsn'}):
        date = today
        ctid = subcode
        name = li.a.text
        price = li.a.em.text
        parent = parentcode  # for future use: node or tree etc.

        item.append({
            'date': date,
            'ctid': ctid,
            'name': name,
            'price': price,
            'parent': parent
        })

        # Top 10 best selling products
        count += 1
        if count > 10:
            break
    return item


if __name__ == '__main__':
    # Get all main category present number
    url = 'https://tw.buy.yahoo.com/help/helper.asp?p=sitemap&hpp=sitemap'
    dom = get_web_page(url, 'big5')
    # Store in sublists
    list_sub, subname = get_sublist(dom)
    # print(list_sub)

    # Initial Empty Dataframe
    col_names = ['date', 'ctid', 'name', 'price', 'parent']
    df = pd.DataFrame(columns=col_names)

    # Loop through it to get all available category id
    for sublist in list_sub:
        url = 'https://tw.buy.yahoo.com/?sub='
        url = str(url+sublist)
        dom = get_web_page(url)
        list_catid, list_catitemid, sub2name, sub3name = get_catid_catitemid(dom, sublist)

        # Main sub extract and load in pandas
        level = 2
        parent = None
        item = get_top_sell(sublist, level, parent)
        temp_pd = pd.DataFrame(item, columns=col_names)
        df = df.append(temp_pd, ignore_index=True)

        # Second sub extract and load in pandas
        for parent, self in list_catid:
            level = 3
            item = get_top_sell(self, level, parent)
            temp_pd = pd.DataFrame(item, columns=col_names)
            df = df.append(temp_pd, ignore_index=True)

        # Third sub extract and load in pandas
        for parent, self in list_catitemid:
            level = 4
            item = get_top_sell(self, level, parent)
            temp_pd = pd.DataFrame(item, columns=col_names)
            df = df.append(temp_pd, ignore_index=True)
        # Remove this "break" to loop all data (now is only first main sub and its offspring)    
        break

    # Validation
    # Parent child relationship
    # print(list_sub)
    # print(list_catid)
    # print(list_catitemid)
    # Corresponding name
    # print(subname)
    # print(sub2name)
    # print(sub3name)
    # Print head
    # print(df.iloc[:50, :])


    # Export to csv
    df.to_csv('data.csv', sep=',', encoding='utf-8')

    # Export to excel
    writer = pd.ExcelWriter('data.xlsx')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

"""
 with open('data.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('date', 'ctid', 'name', 'price', 'parent'))
        for index, row in df.iterrows():
            # comprehensive
            writer.writerow((column for column in row))
"""

