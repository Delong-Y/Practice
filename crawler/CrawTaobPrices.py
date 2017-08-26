import requests
import re

def getHtmlText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('爬取失败')

def parserPage(ilt, html):
    try:
        plt = re.findall(r'\"view_price\":\"[\d\.]*\"', html)
        tlt = re.findall(r'\"raw_title\":\".*?\"', html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ilt.append([price, title])
    except:
        print('')

def printGoodsList(ilt):
    tplt = "{0:<4}\t{1:>8}\t{2:<16}"
    print(tplt.format('序号', '价格（元）', '名称'))
    count = 0
    for lt in ilt:
        count += 1
        print(tplt.format(count, lt[0], lt[1]))

def main(goods, depth):
    url = 'https://s.taobao.com/search?q=' + goods
    infolist = []
    for i in range(depth):
        try:
            turl = url + '&s=' + str(44*i)
            infopage = getHtmlText(turl)
            parserPage(infolist, infopage)
        except:
            continue
    printGoodsList(infolist)

goods = '手表'
depth = 2
main(goods, depth)
