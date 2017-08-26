import requests
import bs4
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return  ''

def getUnivList(ulist, utext):
    soup = BeautifulSoup(utext, 'html.parser')
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            nlist = []
            for td in tr('td'):
                nlist.append(td.string)
            ulist.append(nlist)

def printUnivList(ulist, num):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(tplt.format('排名', '大学', '总分', chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2], chr(12288)))

def main():
    uinfo = []
    url = 'http://www.gaokaopai.com/paihang-otype-1.html'
    num = 20
    utext = getHTMLText(url)
    ulist = getUnivList(uinfo, utext)
    printUnivList(uinfo, num)

main()
