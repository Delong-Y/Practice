from multiprocessing import Pool
import os
import traceback
import bs4
from bs4 import BeautifulSoup
import requests


encoding = 'utf-8'
base_dir = 'D:/crawler/'

def get_page(url, is_text=True, encoding=None):
    proxies = {
        'http': 'http://127.0.0.1:1080',
        'https': 'https://127.0.0.1:1080'
    }
    try:
        r = requests.get(url, proxies=proxies)
        if encoding is not None:
            r.encoding = encoding
        r.raise_for_status()
        return r.text if is_text else r.content
    except:
        traceback.print_exc()

def album_html_parser(html):
    # get the photo album links from the main page
    soup = BeautifulSoup(html, 'html.parser')
    loop_tags = soup.find_all(class_='loop')
    album_links = (loop_tag.div.a['href'] for loop_tag in loop_tags
        if isinstance(loop_tag, bs4.element.Tag))
    return album_links

def photo_html_parser(url):
    # get the photo links of the photo album
    global encoding
    html = get_page(url, encoding=encoding)
    soup = BeautifulSoup(html, 'html.parser')
    photo_tags = soup.find_all('span', class_='photoThum')
    photo_links = [photo_tag.a['href'] for photo_tag in photo_tags
        if isinstance(photo_tag, bs4.element.Tag)]
    return photo_links

def down_photo(url):
    # download the photo of given link and save it to localhost
    global base_dir
    path = url.replace('http://', base_dir)
    dir_path = os.path.dirname(path)
    base_path = os.path.basename(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    if not os.path.exists(path):
        photo = get_page(url, is_text=False)
        with open(path, 'wb') as f:
            f.write(photo)
    # else:
        # print('文件已存在')

def process_way(func, urls):
    workers = 10
    with Pool(workers) as p:
        re = p.map(func, urls)
    return re

def main(depth):
    global encoding

    base_url = 'http://www.xiuren.org'
    base_html = get_page(base_url, encoding=encoding)

    album_links = album_html_parser(base_html)
    photo_all = process_way(photo_html_parser, album_links)

    count = 0
    for photo_links in photo_all:
        try:
            count += 1
            # print(photo_links)
            process_way(down_photo, photo_links)
            # print(count)
            if depth <= count:
                print('Done')
                break
        except:
            traceback.print_exc()
            continue

if __name__ == '__main__':
    main(10)
    # test()
