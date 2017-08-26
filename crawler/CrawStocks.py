import re
import requests
import bs4
from bs4 import BeautifulSoup

def getHtml(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('404')

def parserStockList(codelist_sh, codelist_sz, html):
    soup = BeautifulSoup(html, 'html.parser')
    quote = soup.find('div', "quotebody")
    ul_list = quote.find_all('ul')
    ul_sh = ul_list[0]
    ul_sz = ul_list[1]
    try:
        for li in ul_sh.find_all('li'):
            if isinstance(li, bs4.element.Tag):
                stock = li.string
                codelist_sh.append(re.split('\(|\)', stock)[-2])
        for li in ul_sz.find_all('li'):
            if isinstance(li, bs4.element.Tag):
                stock = li.string
                codelist_sz.append(re.split('\(|\)', stock)[-2])
    except:
        print('loop interupt')

def parserStockHtml(codelist, stockdict):
    for code in codelist[:50]:
        url = 'https://gupiao.baidu.com' + '/stock/sh'+ code + '.html'
        html = getHtml(url)
        # print(html)

        try:
            if html=="":
                continue
            soup  = BeautifulSoup(html, 'html.parser')
            bet_name = soup.find(attrs={'class':"bets-name"}).text.strip()
            price = soup.find(attrs={'class':"_close"}).string.strip()
            # today = soup.find(attrs={'class':"line1"}).dd.text
            # last = soup.find(attrs={'class':"line2"}).dd.text
            # stockdict[bet_name] = [last, today, price]
            stockdict[bet_name] = [price]
        except:
            continue


def printStockInfo(stockdict, num):
    # tplt = "{0:<8}\t{1:>4}\t{2:>4}\t{3:>4}"
    tplt = "{0:<8}\t{1:>4}"
    # print(tplt.format("名字（代码）", "昨收", "今开", "实时"))
    # print(tplt.format("名字（代码）", "昨收", "实时"))
    for (k, v) in stockdict.items:
        # print(tply.format(k, v[0], v[1], v[2]))
        print(tply.format(k, v[0]))

def main():
    listurl = 'http://quote.eastmoney.com/stocklist.html'
    infourl = 'https://gupiao.baidu.com'
    codelist_sh = []
    codelist_sz = []
    stockdict_sh = {}
    stockdict_sz = {}

    listhtml = getHtml(listurl)
    parserStockList(codelist_sh, codelist_sz, listhtml)
    parserStockHtml(codelist_sh, stockdict_sh)
    # printStockInfo(stockdict_sh, 20)
    print(stockdict_sh)
    # for code_sz in codelist_sz:
    #     url = infourl + '/fund/sz' + code_sz + '.html'
    #     html = getHtml(url)
    #     parserStockHtml(stockdict_sz, html)
    #
    # printStockInfo(stockdict_sh, 20)
    # printStockInfo(stockdict_sz, 20)

main()
