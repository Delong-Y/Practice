import os
import traceback
import bs4
from bs4 import BeautifulSoup
import requests

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

def photo_html_parser(html):
    # get the photo links of the photo album
    soup = BeautifulSoup(html, 'html.parser')
    photo_tags = soup.find_all('span', class_='photoThum')
    photo_links = (photo_tag.a['href'] for photo_tag in photo_tags
        if isinstance(photo_tag, bs4.element.Tag))
    return photo_links

def save_page(url, base_dir):
    # download the photo of given link and save it to localhost
    path = url.replace('http://', base_dir)
    dir_path = os.path.dirname(path)
    base_path = os.path.basename(path)
    photo = get_page(url, is_text=False)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            f.write(photo)
    else:
        print('文件已存在')

def main(depth):
    base_url = 'http://www.xiuren.org'
    encoding = 'utf-8'
    base_html = get_page(base_url, encoding=encoding)
    base_dir = 'D:/crawler/'

    album_links = album_html_parser(base_html)
    count = 0
    for album_link in album_links:
        try:
            count += 1
            album_html = get_page(album_link, encoding=encoding)
            photo_links = photo_html_parser(album_html)
            for photo_link in photo_links:
                try:
                    save_page(photo_link, base_dir)
                except:
                    traceback.print_exc()
                    continue
            print(count)
            break if depth <= count else None
        except:
            traceback.print_exc()
            continue
def test():
    # download the first photo of the first album in main page to test the code
    base_url = 'http://www.xiuren.org'
    encoding = 'utf-8'
    base_html = get_page(base_url, encoding=encoding)
    base_dir = 'D:/crawler/'

    album_links = album_html_parser(base_html)
    count = 0

    album_list = [album for album in album_links]
    album_html = get_page(album_list[0], encoding=encoding)
    photo_links = photo_html_parser(album_html)
    photo_list = [photo for photo in photo_links]
    save_page(photo_list[0], base_dir)
    print(count)

if __name__ == '__main__':
    main(2)
